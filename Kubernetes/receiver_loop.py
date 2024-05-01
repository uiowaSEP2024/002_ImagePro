import time

import pyorthanc
import argparse
from kubernetes import client, config

from util_functions import (
    OrthancConnectionException,
    setup_custom_logger,
    check_study_has_properties,
)


class ReceiverLoop:
    # Class Attributes
    TIME_BETWEEN_CONNECTIONS = 5
    STARTING_MAX_RETRIES = 10
    QUERY_INTERVAL = 5

    def __init__(
        self,
        orthanc_url: str,
        api_key: str,
        hospital_mapping_file: str,
        # study_config_file: str,
        backend_url: str,
    ):
        self.continue_running = True

        self.orthanc_url = orthanc_url
        self.internal_orthanc = None
        self.max_retries = self.STARTING_MAX_RETRIES
        self.logger = setup_custom_logger("receiver_loop")
        self.internal_orthanc: pyorthanc.Orthanc | None = None
        self.api_key = api_key
        self.backend_url = backend_url
        self.hospital_mapping_file = hospital_mapping_file
        # self.study_config_file = study_config_file
        self._init_orthanc_connection()
        self.kube_job_name = "study-job"
        try:
            # Use in-cluster configuration if running inside a pod
            config.load_incluster_config()
        except config.ConfigException:
            # Use kubeconfig file if running outside the cluster (e.g., for local debugging)
            config.load_kube_config()
        self.kube_api_client = client.BatchV1Api()
        self.studies_list = []

    def _init_orthanc_connection(self):
        while self.max_retries > 0 and not self.internal_orthanc:
            try:
                self.internal_orthanc = pyorthanc.Orthanc(self.orthanc_url)
            except TimeoutError:
                self.logger.error(
                    f"Connection to Orthanc timed out sleeping for {self.QUERY_INTERVAL} seconds"
                )
                self.max_retries -= 1
                time.sleep(self.TIME_BETWEEN_CONNECTIONS)
            except Exception as orthanc_e:
                self.max_retries -= 1
                self.logger.error(f"ERROR connecting to Orthanc: {orthanc_e}")
                time.sleep(self.TIME_BETWEEN_CONNECTIONS)
        if not self.internal_orthanc:
            raise OrthancConnectionException(
                f"Receiver Loop failed to connect to Orthanc at {self.orthanc_url} after {self.max_retries} retries"
            )
        self.logger.info("connected to orthanc")

    def _get_hospital_return_aet_mapping(self):
        # TODO implement this with reading in a dictionary from a file
        # TODO: this probably should be a mapping, ex. {"EXAMPLE_TOOL": "EXAMPLE_HOSPITAL_NAME"}
        print(f"Reading in hospital mapping from {self.hospital_mapping_file}")
        # TODO: for now reuturn id of the original Hospital
        return "EXAMPLE_HOSPITAL_NAME"

    def _spawn_single_study_run(self, study_id: str):
        # Generate a unique job name
        job_name = f"{self.kube_job_name}-{study_id}"

        # Define the job manifest with arguments
        job_manifest = {
            "apiVersion": "batch/v1",
            "kind": "Job",
            "metadata": {"name": job_name, "namespace": "default"},
            "spec": {
                "ttlSecondsAfterFinished": 10,
                "template": {
                    "metadata": {"name": job_name},
                    "spec": {
                        "containers": [
                            {
                                "name": "script-container",
                                "image": "study:latest",
                                "imagePullPolicy": "IfNotPresent",
                                "args": [
                                    "--orthanc_url",
                                    self.orthanc_url,
                                    "--study_id",
                                    study_id,
                                    "--tracker_api_key",
                                    self.api_key,
                                    # "--study_config_file",
                                    # self.study_config_file,
                                    "--backend_url",
                                    self.backend_url,
                                    "--original_hospital_id",
                                    self._get_hospital_return_aet_mapping(),
                                ],
                                "volumeMounts": [
                                    {"name": "data-volume", "mountPath": "/data"}
                                ],
                                "resources": {
                                    "limits": {"memory": "512Mi", "cpu": "500m"}
                                },
                            }
                        ],
                        "automountServiceAccountToken": True,
                        "restartPolicy": "Never",
                        "serviceAccountName": "test-service-account",
                        "volumes": [
                            {
                                "name": "data-volume",
                                "persistentVolumeClaim": {"claimName": "data-pvc"},
                            }
                        ],
                    },
                },
            },
        }

        # Create the job
        try:
            self.kube_api_client.create_namespaced_job(
                body=job_manifest, namespace="default"
            )
            self.logger.info(f"Job created. Name='{job_name}'")
        except Exception as e:
            self.logger.info(f"Job creation failed: {e}")
        time.sleep(5)  # Adjust time based on observed API behavior

    def _check_for_new_studies(self):
        try:
            studies = pyorthanc.find_studies(self.internal_orthanc)
            logger.info(f"Studies from orthanc: {studies}")
        except Exception as e:
            self.logger.error(f"Error finding studies: {e}")
            return
        for study in studies:
            if check_study_has_properties(study):
                self.logger.info(f"Found study {study.id_}")
                logger.info(f"Studies list: {self.studies_list}")
                if study.id_ not in self.studies_list:
                    logger.info(f"Spawning study {study.id_}")
                    self.studies_list.append(study.id_)
                    self._spawn_single_study_run(study.id_)
                else:
                    self.logger.info(
                        f"Study {study.id_} already in studies_dict skipping"
                    )
            else:
                raise ValueError(
                    f"Study {study.id_} does not have the required properties"
                )
        else:
            self.logger.info("No studies found")

    def _check_job_completion(self, api_instance, study_id: str):
        self.logger.info("Checking study job completion status...")
        job_name = f"{self.kube_job_name}-{study_id}"
        completed = False
        try:
            res = api_instance.read_namespaced_job_status(job_name, "default")
            if res.status.succeeded == 1:
                self.logger.info("Job completed successfully.")
                completed = True
            elif res.status.failed is not None and res.status.failed > 0:
                self.logger.info("Job failed.")
                completed = True
            else:
                self.logger.info("Job still running.")
                completed = False
        except client.exceptions.ApiException as e:
            self.logger.info(f"Error checking job status: {e}")
        return completed

    def check_for_completed_studies(self):
        studies_to_remove = []
        for study_id in self.studies_list:
            if self._check_job_completion(self.kube_api_client, study_id):
                studies_to_remove.append(study_id)

        logger.info(f"Studies to remove: {studies_to_remove}")
        for study_id in studies_to_remove:
            self.studies_list.remove(study_id)
            self.logger.info(
                f"Study {study_id} has been removed from studies_dict after processing."
            )

        self.logger.info("No completed studies found")


logger = setup_custom_logger("initialization")
logger.info("Start of Receiver Loop main")

parser = argparse.ArgumentParser()
parser.add_argument("--orthanc_url", type=str, required=True)
parser.add_argument("--api_key", type=str, required=True)
parser.add_argument("--hospital_mapping_file", type=str, required=True)
# parser.add_argument("--study_config_file", type=str, required=True)
parser.add_argument("--backend_url", type=str, required=True)
args = parser.parse_args()

logger.info(args)

receiver_loop = ReceiverLoop(
    orthanc_url=args.orthanc_url,
    api_key=args.api_key,
    hospital_mapping_file=args.hospital_mapping_file,
    # study_config_file=args.study_config_file,
    backend_url=args.backend_url,
)


while receiver_loop.continue_running:
    logger.info("Checking for new studies")
    receiver_loop._check_for_new_studies()
    logger.info("Checking for completed studies")
    receiver_loop.check_for_completed_studies()
    logger.info("Waiting for five seconds before checking again...")
    time.sleep(receiver_loop.QUERY_INTERVAL)
