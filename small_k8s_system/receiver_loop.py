import time

import pyorthanc
import argparse
import logging
from kubernetes import client

# from study import SingleStudyRun
from util_functions import (
    OrthancConnectionException,
    setup_custom_logger,
)

# TODO: For now comment out all logic not related to Orthanc connection
# if os.environ.get("DOCKER_ENV"):
#     from util_functions import (
#         check_study_has_properties,
#         OrthancConnectionException,
#         setup_custom_logger,
#     )
# else:
#     from internal_servers.study import SingleStudyRun
#     from internal_servers.util_functions import (
#         check_study_has_properties,
#         OrthancConnectionException,
#         setup_custom_logger,
#     )


def check_job_completion(api_instance, job_name):
    # TODO: we need to investigate how to check/assign specific kuberneted job id
    # TODO: as there might be many instances of study being run we need to check for a specific one
    # TODO: ideally we would create a job with an assign id and create a mapping between orthanc study and job id
    print("Checking study job completion status...")
    completed = False
    try:
        res = api_instance.read_namespaced_job_status(job_name, "default")
        if res.status.succeeded == 1:
            print("Job completed successfully.")
            completed = True
        elif res.status.failed is not None and res.status.failed > 0:
            print("Job failed.")
            completed = True
        else:
            print("Job still running.")
            completed = False
    except client.exceptions.ApiException as e:
        print(f"Error checking job status: {e}")
    return completed


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
        study_config_file: str,
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
        self.study_config_file = study_config_file
        self._init_orthanc_connection()
        # self.studies_dict: dict[str, SingleStudyRun] = {}

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

    # def _spawn_single_study_run(self, study_id: str):
    # TODO: this code will have to be replaced with the Kubernetes API Job manifest.
    # TODO: the study code in the future will have to be rewritten to implement actual logic and take arguments as the
    # TODO: old function below

    #     single_study_run = SingleStudyRun(
    #         orthanc_url=self.orthanc_url,
    #         study_id=study_id,
    #         tracker_api_key=self.api_key,
    #         study_config_file=self.study_config_file,
    #         hospital_mapping_file=self.hospital_mapping_file,
    #         backend_url=self.backend_url,
    #     )
    #     return single_study_run

    # def _check_for_new_studies(self):
    #     try:
    #         studies = pyorthanc.find_studies(self.internal_orthanc)
    #     except Exception as e:
    #         self.logger.error(f"Error finding studies: {e}")
    #         return
    #     for study in studies:
    #         if check_study_has_properties(study):
    #             self.logger.info(f"Found study {study.id_}")
    #             if study.id_ not in self.studies_dict:
    #                 logger.info(f"Spawning study {study.id_}")
    #                 # self.studies_dict[study.id_] = self._spawn_single_study_run(
    #                 #     study.id_
    #                 # )
    #             else:
    #                 self.logger.info(
    #                     f"Study {study.id_} already in studies_dict skipping"
    #                 )
    #         else:
    #             raise ValueError(
    #                 f"Study {study.id_} does not have the required properties"
    #             )
    #     else:
    #         print("No studies found")

    def check_for_completed_studies(self):
        studies_to_remove = []
        for study_id, single_study_run in self.studies_dict.items():
            # TODO: use the ubernetes job completion checking
            if not single_study_run.get_study_is_in_progress():
                studies_to_remove.append(study_id)

        for study_id in studies_to_remove:
            self.studies_dict.pop(study_id)
            self.logger.info(
                f"Study {study_id} has been removed from studies_dict after processing for {single_study_run.get_study_is_completed()}"
            )


logger = setup_custom_logger("initialization")
logger = logging.getLogger("initialization")
logger.info("Start of Receiver Loop main")

parser = argparse.ArgumentParser()
parser.add_argument("--orthanc_url", type=str, required=True)
parser.add_argument("--api_key", type=str, required=True)
parser.add_argument("--hospital_mapping_file", type=str, required=True)
parser.add_argument("--study_config_file", type=str, required=True)
parser.add_argument("--backend_url", type=str, required=True)
args = parser.parse_args()

logger.info(args)

receiver_loop = ReceiverLoop(
    orthanc_url=args.orthanc_url,
    api_key=args.api_key,
    hospital_mapping_file=args.hospital_mapping_file,
    study_config_file=args.study_config_file,
    backend_url=args.backend_url,
)


while receiver_loop.continue_running:
    logger.info("Loop is running. Wait 5s")
    time.sleep(5)
    # receiver_loop._check_for_new_studies()
    # receiver_loop.check_for_completed_studies()
    # time.sleep(receiver_loop.QUERY_INTERVAL)
