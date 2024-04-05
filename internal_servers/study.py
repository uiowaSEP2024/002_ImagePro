import zipfile
from enum import Enum
from pathlib import Path

import pyorthanc
import logging
import time
from internal_servers.orthanc_data_logging import OrthancStudyLogger
from internal_servers.util_functions import (
    OrthancConnectionException,
    format_time_delta_human_readable,
)


class StudyState(Enum):
    """
    Enum for the state of the study
    """

    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    ERROR = "Error"
    FAILED = "Failed"


class SingleStudyRun:
    def __init__(
        self,
        orthanc_url: str,
        study_id: str,
        tracker_api_key: str,
        study_config_file: str,
        hospital_mapping_file: str,
    ):
        self.orthanc_url = orthanc_url
        self.study_status = StudyState.IN_PROGRESS
        self.study_id = study_id
        self.is_processed = False
        self.tracker_api_key = tracker_api_key
        self.study_config_file = study_config_file

        self.study_dir = Path(f"/tmp/{self.study_id}")
        self.study_dir.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(
            "receiver_loop"
        )  # Possibly change this to a different logger its fine for now
        self.hospital_mapping = self._get_hospital_return_aet_mapping(
            hospital_mapping_file
        )
        self.study: pyorthanc.Study | None = (
            None  # Should be overwritten the _init_study_object function
        )
        self.orthanc: pyorthanc.Orthanc | None = None
        self.start_time = time.time()
        self.end_time: time.time | None = None

        self.max_retries: int = 5
        self._init_orthanc_connection()
        self._init_study_object()
        self._init_study_logger()

    # Boilerplate code for the study state
    def get_study_is_in_progress(self) -> bool:
        return self.study_status == StudyState.IN_PROGRESS

    def get_study_is_completed(self) -> bool:
        return self.study_status == StudyState.COMPLETED

    def get_study_is_errored(self) -> bool:
        return self.study_status == StudyState.ERROR

    def get_study_is_failed(self) -> bool:
        return self.study_status == StudyState.FAILED

    def get_study_status(self) -> StudyState:
        return self.study_status

    def _study_completed_processing(self) -> None:
        self.study_status = StudyState.COMPLETED
        self.end_time = time.time()
        self.logger.info(f"Study {self.study_id}: {self._get_time_processing_str()}")

    def _get_download_dir(self) -> Path:
        return self.study_dir / "download"

    def _get_extract_dir(self) -> Path:

        return self.study_dir / "extract"

    def _get_time_processing_str(self) -> str:
        time_str = ""
        if self.end_time > 0:
            time_str += f"Processing Completed in :{format_time_delta_human_readable(self.end_time - self.start_time)}"
        else:
            time_str += f"Processing still in progress, been running for {format_time_delta_human_readable(time.time() - self.start_time)}"
        return time_str

    def _get_hospital_return_aet_mapping(self, hopital_mapping_file: str):
        # TODO implement this with reading in a dictionary from a file

        print(f"Reading in hospital mapping from {hopital_mapping_file}")
        return {"EXAMPLE_TOOL": "EXAMPLE_TOOL"}

    def study_is_stable(self) -> bool:
        """
        Check if the study is stable.

        This function checks if the study is stable by fetching the main information
        of the study and checking the "IsStable" key.
        param study: The study to check.
        return: True if the study is stable, False otherwise.
        """
        is_stable: bool = False
        try:
            is_stable = self.study.get_main_information().get("IsStable", False)
        except Exception as get_main_info_e:
            msg: str = f"ERROR getting study main information for {self.study_id}: {get_main_info_e}"
            self.logger.info(msg)
        return is_stable

    def study_has_properties(self) -> bool:
        # TODO Check if I can find this information without fetching the series just directly from the stuyd_object
        for series in self.study.series:
            if (
                series.get_main_information()["MainDicomTags"]["SeriesDescription"]
                == "PROPERTIES"
            ):
                return True
        return False

    def _init_study_logger(self):
        self.study_job_tracker = OrthancStudyLogger(
            hospital_id=self.hospital_mapping["EXAMPLE_TOOL"],  # TODO make this dynamic
            study_id=self.study_id,
            tracker_api_key=self.tracker_api_key,
            study_config_file=self.study_config_file,
        )

    def _init_orthanc_connection(self) -> None:
        while self.max_retries > 0 and not self.orthanc:
            try:
                self.orthanc = pyorthanc.Orthanc(self.orthanc_url)
            except Exception as orthanc_e:
                self.max_retries -= 1
                self.logger.error(f"ERROR connecting to Orthanc: {orthanc_e}")
                time.sleep(5)
        if not self.orthanc:
            raise OrthancConnectionException(
                f"Study {self.study_id} failed to connect to Orthanc at {self.orthanc_url} after {self.max_retries} retries"
            )

    def _init_study_object(self):
        try:
            studies = pyorthanc.find(
                self.orthanc,
                study_filter=lambda study: study.id_ == self.study_id,
            )

            if len(studies) > 1:
                self.logger.error(
                    f"ERROR: Found more than one study with ID {self.study_id}"
                )
                self.study_status = StudyState.ERROR
            else:
                self.study = studies[0]
                self.logger.info(f"Study {self.study_id} found")
        except Exception as e:
            self.logger.error(f"ERROR getting study {self.study_id} from Orthanc: {e}")
            self.study_status = StudyState.ERROR

    def _download_study(self) -> Path:
        """
        Downloads a DICOM study from an Orthanc server using pyorthanc and saves it to a specified directory as a ZIP file.

        Args:
        - download_dir (str): The directory path where the ZIP file will be saved.

        This function first attempts to download the entire DICOM study associated with the given
        study_id from the Orthanc server in ZIP format using the pyorthanc client. If the download is successful,
        the ZIP file is saved to the specified directory. If the directory does not exist, it is created.

        The function prints a message indicating the success or failure of the download operation.
        """
        # Ensure the Path object is used for path operations
        download_dir = self._get_download_dir()
        download_dir.mkdir(parents=True, exist_ok=True)
        # Define the path for the ZIP file
        zip_path = download_dir / f"{self.study_id}.zip"

        try:
            # Use pyorthanc to download the study as a ZIP archive
            study_archive = self.orthanc.get_studies_id_archive(self.study_id)

            # Save the ZIP file to the specified path
            with open(zip_path, "wb") as f:
                f.write(study_archive)
            self.logger.info(f"Downloaded and saved DICOM study ZIP to {zip_path}")
            return zip_path
        except Exception as e:
            self.logger.info(
                f"Error to download DICOM study for study ID {self.study_id}. Error: {e}"
            )

    def _unzip_study(self):
        """
        Extracts a ZIP file containing a DICOM study into a specified directory.

        Args:
        - zip_path (str): The path to the ZIP file to be extracted.
        - extract_dir (str): The directory path where the contents of the ZIP file will be extracted.

        This function attempts to extract all the contents of the ZIP file specified by zip_path
        into the directory specified by extract_dir. If the directory does not exist, it is created.

        The function prints a message indicating the success or failure of the extraction operation.
        """

        # Ensure the Path objects are used for path operations
        zip_path = self._get_download_dir() / f"{self.study_id}.zip"
        extract_dir = self._get_extract_dir()
        extract_dir.mkdir(
            parents=True, exist_ok=True
        )  # Ensure the extraction directory exists

        try:
            # Open the ZIP file and extract its contents
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_dir)
            self.logger.info(f"Extracted DICOM study to {extract_dir}")
        except Exception as e:
            self.logger.info(f"Error to extract ZIP file {zip_path}. Error: {e}")

    def process_study(self):
        if self.study_status != StudyState.IN_PROGRESS:
            self.logger.error(
                f"ERROR: Study {self.study_id} is not in progress. Not processing"
            )
        if self.study_is_stable():
            self.study_job_tracker.update_step_status(1, "Complete")
