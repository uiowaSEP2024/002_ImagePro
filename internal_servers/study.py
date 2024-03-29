from enum import Enum

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
        self.logger = logging.getLogger(
            "receiver_loop"
        )  # Possibly change this to a different logger its fine for now
        self.hospital_mapping = self._get_hospital_return_aet_mapping(
            hospital_mapping_file
        )
        self.async_orthanc: pyorthanc.AsyncOrthanc | None = None
        self.start_time = time.time()
        self.end_time: time.time | None = None

        self.max_retries: int = 5
        self._init_orthanc_connection()

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

    def study_is_stable(self, study: pyorthanc.Study) -> bool:
        """
        Check if the study is stable.

        This function checks if the study is stable by fetching the main information
        of the study and checking the "IsStable" key.
        param study: The study to check.
        return: True if the study is stable, False otherwise.
        """
        is_stable: bool = False
        try:
            is_stable = study.get_main_information().get("IsStable", False)
        except Exception as get_main_info_e:
            msg: str = f"ERROR getting study main information for {study.id_}: {get_main_info_e}"
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

    def _init_study_logger(self, tracker_api_key: str, study_config_file: str):
        self.study_logger = OrthancStudyLogger(
            hospital_id=self.hospital_mapping["EXAMPLE_TOOL"],  # TODO make this dynamic
            study_id=self.study_id,
            tracker_api_key=tracker_api_key,
            study_config_file=study_config_file,
        )

    def _init_orthanc_connection(self) -> None:
        while self.max_retries > 0 and not self.async_orthanc:
            try:
                self.async_orthanc = pyorthanc.AsyncOrthanc(self.orthanc_url)
            except Exception as orthanc_e:
                self.max_retries -= 1
                self.logger.error(f"ERROR connecting to Orthanc: {orthanc_e}")
                time.sleep(5)
        if not self.async_orthanc:
            raise OrthancConnectionException(
                f"Study {self.study_id} failed to connect to Orthanc at {self.orthanc_url} after {self.max_retries} retries"
            )

    async def _init_study_object(self):
        try:
            studies = await pyorthanc.find(
                self.async_orthanc,
                study_filter=lambda study: study.id_ == self.study_id,
            )
            if len(studies) > 1:
                self.logger.error(
                    f"ERROR: Found more than one study with ID {self.study_id}"
                )
                self.study_status = StudyState.ERROR
        except Exception as e:
            self.logger.error(f"ERROR getting study {self.study_id} from Orthanc: {e}")
            self.study_status = StudyState.ERROR
