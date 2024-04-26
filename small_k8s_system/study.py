import zipfile
from enum import Enum
from pathlib import Path
from util_functions import (
    format_time_delta_human_readable,
    OrthancConnectionException,
    setup_custom_logger,
)

from study_tracking import StudyTracker
import argparse
import pyorthanc
import time
import shutil
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
        backend_url: str,
        original_hospital_id: str,
    ):
        self.orthanc_url = orthanc_url
        self.study_status = StudyState.IN_PROGRESS
        self.study_id = study_id
        self.is_processed = False
        self.tracker_api_key = tracker_api_key
        self.study_config_file = study_config_file
        self.backend_url = backend_url
        self.original_hospital_id = original_hospital_id

        # Setup the study directories
        # TODO: Ensure that this is in the path expected by the PVC
        self.study_dir = Path(f"/data/{self.study_id}")
        self.study_dir.mkdir(parents=True, exist_ok=True)

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
        self.product_name = "brainmask-tool"
        self.product_job_name = f"{self.product_name}-job-{self.study_id}"
        self.product_image = "brainmasktool_light:v0.1"
        self.product_command = ["python", "brainmask_tool.py"]
        self.product_job_args = [
            "-i",
            self.study_id,
            "-s",
            self._get_extract_dir().as_posix(),
            "-o",
            f"{self.study_dir}/{self.product_name}-output",
        ]

        self.logger = setup_custom_logger(f"study_{self.study_id}")

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

    def _init_study_logger(self):
        try:
            self.study_job_tracker = StudyTracker(
                hospital_id=self.original_hospital_id,  # TODO make this dynamic
                study_id=self.study_id,
                tracker_api_key=self.tracker_api_key,
                study_config_file=self.study_config_file,
                backend_url=self.backend_url,
            )
            self.logger.info(f"Successfully initialized study tracker for study {self.study_id}")
        except Exception as e:
            self.logger.error(f"ERROR initializing study tracker for study {self.study_id}: {e}")

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

    def _delete_study_data(self):
        """
        Deletes the study data from the system.
        """
        shutil.rmtree(self.study_dir)
        self.logger.info(f"Deleted study data for study ID {self.study_id}")

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

    def _check_job_completion(self) -> bool | Exception:
        self.logger.info("Checking job completion status...")
        completed = False
        max_retries = 20
        attempt = 0
        while attempt < max_retries and not completed:
            try:
                res = self.kube_api_client.read_namespaced_job_status(
                    self.product_job_name, "default"
                )
                self.logger.info(f"res status: {res.status}")
                if res.status.succeeded == 1:
                    self.logger.info("Job completed successfully.")
                    completed = True
                elif res.status.failed is not None and res.status.failed > 0:
                    self.logger.info("Job failed.")
                    completed = True
                else:
                    self.logger.info(
                        "Job still running. Checking again in 5 seconds..."
                    )
                    time.sleep(10)
                attempt += 1
            except client.exceptions.ApiException as e:
                self.logger.info(f"Error checking job status: {e}")
                return e
        return completed

    def _upload_data_to_internal(self) -> None | Exception:
        """
        Uploads DICOM files from a specified directory back to an Orthanc server.
        """
        # Iterate over each file in the directory and upload it
        directory = self._get_deliverables_dir()
        for file_path in directory.rglob(
            "*.dcm"
        ):  # Assuming DICOM files have .dcm extension
            try:
                with open(file_path, "rb") as file:
                    result = self.orthanc.post_instances(file.read())
                    self.logger.debug(result.get("Status"))
                    self.logger.debug(result)
                self.logger.info(f"Successfully uploaded {file_path.name} to Orthanc.")
                return None
            except Exception as e:
                self.logger.error(f"Failed to upload {file_path.name}. Error: {e}")
                return e

    def _return_to_original_hospital(self):
        """
        Return data to the original sender - Hospital PACS
        """
        response = self.orthanc.post_modalities_id_store(
            self.original_hospital_id, self.study_id
        )
        self.logger.info(response)

    def process_study(self):
        # This implementation follows the tested orthanc_receiver_agent.py logic
        while True:
            # Ensure the study is stable
            if self._study_is_stable():
                self.study_job_tracker.update_step_status(1, "Complete")
                # Download and extract the study data
                if self.study_job_tracker.step_is_ready(2):
                    self.study_job_tracker.update_step_status(2, "In progress")
                    # TODO: ensure that the download status is not an exception
                    # TODO: Audrey, I am not sure about this code, it might cause some troubles
                    download_status = self._download_study()
                    extraction_status = self._unzip_study()
                    if isinstance(download_status, Exception):
                        self.study_job_tracker.update_step_status(
                            2, "Error", str(download_status)
                        )
                        break
                    else:
                        if isinstance(extraction_status, Exception):
                            self.study_job_tracker.update_step_status(
                                2, "Error", str(download_status)
                            )
                            break
                        else:
                            self.study_job_tracker.update_step_status(2, "Complete")
                # Process study data using the product job
                if self.study_job_tracker.step_is_ready(3):
                    self.study_job_tracker.update_step_status(3, "In progress")
                    self._create_product_job()
                    job_status = self._check_job_completion()
                    if job_status:
                        self.study_job_tracker.update_step_status(3, "Complete")
                    else:
                        self.study_job_tracker.update_step_status(
                            3, "Error", str(job_status)
                        )
                        break
                # Return data to internal Orthanc
                if self.study_job_tracker.step_is_ready(4):
                    self.study_job_tracker.update_step_status(4, "In progress")
                    upload_status = self._upload_data_to_internal()
                    if isinstance(upload_status, Exception):
                        self.study_job_tracker.update_step_status(
                            4, "Error", str(upload_status)
                        )
                    else:
                        self._return_to_original_hospital()
                        self.study_job_tracker.update_step_status(4, "Complete")
                    self.orthanc.delete_studies_id(self.study_id)
                    break
            else:
                self.logger.info("Study not stable yet, waiting 10 seconds")
                time.sleep(10)

        # # This implementation follows the tested orthanc_receiver_agent.py logic
        # while True:
        #     # Ensure the study is stable
        #     if self._study_is_stable():
        #         # Download and extract the study data
        #         download_status = self._download_study()
        #         extraction_status = self._unzip_study()
        #         if isinstance(download_status, Exception):
        #             break
        #         else:
        #             if isinstance(extraction_status, Exception):
        #                 break
        #             else:
        #                 pass
        #         # Process study data using the product job
        #         self._create_product_job()
        #         job_status = self._check_job_completion()
        #         self.logger.info(f"Job status: {job_status}")
        #         if job_status:
        #             pass
        #         else:
        #             break
        #         # Return data to internal Orthanc
        #         upload_status = self._upload_data_to_internal()
        #         if isinstance(upload_status, Exception):
        #             break
        #         else:
        #             self._return_to_original_hospital()
        #         self.orthanc.delete_studies_id(self.study_id)
        #         break
        #     else:
        #         self.logger.info("Study not stable yet, waiting 10 seconds")
        #         time.sleep(10)

        # Ensure data deletion
        self._delete_study_data()


if __name__ == "__main__":
    # Parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--orthanc_url", type=str, required=True)
    parser.add_argument("--study_id", type=str, required=True)
    parser.add_argument("--tracker_api_key", type=str, required=True)
    parser.add_argument("--study_config_file", type=str, required=True)
    parser.add_argument("--backend_url", type=str, required=True)
    parser.add_argument("--original_hospital_id", type=str, required=True)
    args = parser.parse_args()

    # Create the study job
    study_job = SingleStudyJob(
        orthanc_url=args.orthanc_url,
        study_id=args.study_id,
        tracker_api_key=args.tracker_api_key,
        study_config_file=args.study_config_file,
        backend_url=args.backend_url,
        original_hospital_id=args.original_hospital_id,
    )

    # Process the study
    study_job.process_study()
