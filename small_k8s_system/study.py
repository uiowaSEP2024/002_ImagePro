import zipfile
from enum import Enum
from pathlib import Path
from util_functions import format_time_delta_human_readable, OrthancConnectionException, setup_custom_logger
from study_tracking import StudyTracker
import argparse
import pyorthanc
import logging
import time
from kubernetes import client, config


class StudyState(Enum):
    """
    Enum for the state of the study
    """

    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    ERROR = "Error"
    FAILED = "Failed"


class SingleStudyJob:
    def __init__(
        self,
        orthanc_url: str,
        study_id: str,
        tracker_api_key: str,
        study_config_file: str,
        hospital_mapping_file: str,
        backend_url: str,
    ):
        self.orthanc_url = orthanc_url
        self.study_status = StudyState.IN_PROGRESS
        self.study_id = study_id
        self.is_processed = False
        self.tracker_api_key = tracker_api_key
        self.study_config_file = study_config_file
        self.backend_url = backend_url

        # Setup Kubernetes client
        try:
            # Use in-cluster configuration if running inside a pod
            config.load_incluster_config()
        except config.ConfigException:
            # Use kubeconfig file if running outside the cluster (e.g., for local debugging)
            config.load_kube_config()
        self.kube_api_client = client.BatchV1Api()

        # Setup kubernetes product job variables
        # Trigger the BrainMask Tool job with dynamic arguments
        self.product_job_name = f"brainmask-tool-job-{self.study_id}"
        self.product_image = "brainmasktool_light:v0.1"
        self.product_command = ["python", "brainmask_tool.py"]
        self.product_job_args = ["-i", "abc123", "-s", "/data/input", "-o", "/data/output"]

        # Setup the study directories
        # TODO: Ensure that this is in the path expected by the PVC
        self.study_dir = Path(f"/data/{self.study_id}")
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

    def _get_deliverables_dir(self) -> Path:
        return self.study_dir / "deliverables"

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

    def _study_is_stable(self) -> bool:
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
        self.study_job_tracker = StudyTracker(
            hospital_id=self.hospital_mapping["EXAMPLE_TOOL"],  # TODO make this dynamic
            study_id=self.study_id,
            tracker_api_key=self.tracker_api_key,
            study_config_file=self.study_config_file,
            backend_url=self.backend_url,
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

    def _download_study(self) -> None | Exception:
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
            return None
        except Exception as e:
            self.logger.info(
                f"Error to download DICOM study for study ID {self.study_id}. Error: {e}"
            )
            return e

    def _unzip_study(self) -> None | Exception:
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
            return None
        except Exception as e:
            self.logger.info(f"Error to extract ZIP file {zip_path}. Error: {e}")
            return e

    def _create_product_job(self):
        self.logger.info("Creating the job with dynamic arguments...")
        job_manifest = {
            "apiVersion": "batch/v1",
            "kind": "Job",
            "metadata": {"name": self.product_job_name, "namespace": "default"},
            "spec": {
                "template": {
                    "spec": {
                        "containers": [
                            {
                                "name": self.product_job_name,
                                "image": self.product_image,
                                "command": self.product_command,
                                "args": self.product_job_args,
                                "volumeMounts": [
                                    {"name": "data-volume", "mountPath": "/data"}
                                ],
                            }
                        ],
                        "restartPolicy": "Never",
                        "volumes": [
                            {
                                "name": "data-volume",
                                "persistentVolumeClaim": {"claimName": "data-pvc"},
                            }
                        ],
                    }
                }
            },
        }

        api_response = self.kube_api_client.create_namespaced_job(
            body=job_manifest, namespace="default"
        )
        self.logger.info(f"Job '{api_response.metadata.name}' created.")
        # Wait a few seconds after job creation before returning
        time.sleep(5)  # Adjust time based on observed API behavior

    def _check_job_completion(self):
        self.logger.info("Checking job completion status...")
        completed = False
        while not completed:
            try:
                res = self.kube_api_client.read_namespaced_job_status(self.product_job_name, "default")
                if res.status.succeeded == 1:
                    self.logger.info("Job completed successfully.")
                    completed = True
                elif res.status.failed is not None and res.status.failed > 0:
                    self.logger.info("Job failed.")
                    completed = True
                else:
                    self.logger.info("Job still running. Checking again in 5 seconds...")
                    time.sleep(10)
            except client.exceptions.ApiException as e:
                self.logger.info(f"Error checking job status: {e}")
                break
        return completed

    def process_study(self):
        if self.study_status != StudyState.IN_PROGRESS:
            self.logger.error(
                f"ERROR: Study {self.study_id} is not in progress. Not processing"
            )
        if self.study_is_stable():
            self.study_job_tracker.update_step_status(1, "Complete")


if __name__ == "__main__":
    # Setup the logger and initial statements
    logger = setup_custom_logger("study job initialization")
    logger.info("Start of the script")

    # Parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--orthanc_url", type=str, required=True)
    parser.add_argument("--study_id", type=str, required=True)
    parser.add_argument("--tracker_api_key", type=str, required=True)
    parser.add_argument("--hospital_mapping_file", type=str, required=True)
    parser.add_argument("--study_config_file", type=str, required=True)
    parser.add_argument("--backend_url", type=str, required=True)
    args = parser.parse_args()

    logger.info(args)

    # Create the study job
    study_job = SingleStudyJob(
        orthanc_url=args.orthanc_url,
        study_id=args.study_id,
        tracker_api_key=args.tracker_api_key,
        study_config_file=args.study_config_file,
        hospital_mapping_file=args.hospital_mapping_file,
        backend_url=args.backend_url,
    )




    # Process the study
