import time

import pyorthanc
import os
import argparse

if os.environ.get("DOCKER_ENV"):
    from study import SingleStudyRun
    from util_functions import (
        check_study_has_properties,
        OrthancConnectionException,
        setup_custom_logger,
    )
else:

    from internal_servers.study import SingleStudyRun
    from internal_servers.util_functions import (
        check_study_has_properties,
        OrthancConnectionException,
        setup_custom_logger,
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
        self.studies_dict: dict[str, SingleStudyRun] = {}

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

    def _spawn_single_study_run(self, study_id: str):
        single_study_run = SingleStudyRun(
            orthanc_url=self.orthanc_url,
            study_id=study_id,
            tracker_api_key=self.api_key,
            study_config_file=self.study_config_file,
            hospital_mapping_file=self.hospital_mapping_file,
            backend_url=self.backend_url,
        )
        return single_study_run

    def _check_for_new_studies(self):
        studies = pyorthanc.find_studies(self.internal_orthanc)
        for study in studies:
            if check_study_has_properties(study):
                self.logger.info(f"Found study {study.id_}")
                if study.id_ not in self.studies_dict:
                    self.studies_dict[study.id_] = self._spawn_single_study_run(
                        study.id_
                    )
                else:
                    self.logger.info(
                        f"Study {study.id_} already in studies_dict skipping"
                    )
            else:
                raise ValueError(
                    f"Study {study.id_} does not have the required properties"
                )

    def check_for_completed_studies(self):
        studies_to_remove = []
        for study_id, single_study_run in self.studies_dict.items():
            if not single_study_run.get_study_is_in_progress():
                studies_to_remove.append(study_id)

        for study_id in studies_to_remove:
            self.studies_dict.pop(study_id)
            self.logger.info(
                f"Study {study_id} has been removed from studies_dict after processing for {single_study_run.get_study_is_completed()}"
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--orthanc_url", type=str, required=True)
    parser.add_argument("--api_key", type=str, required=True)
    parser.add_argument("--hospital_mapping_file", type=str, required=True)
    parser.add_argument("--study_config_file", type=str, required=True)
    parser.add_argument("--backend_url", type=str, required=True)
    args = parser.parse_args()

    receiver_loop = ReceiverLoop(
        orthanc_url=args.orthanc_url,
        api_key=args.api_key,
        hospital_mapping_file=args.hospital_mapping_file,
        study_config_file=args.study_config_file,
        backend_url=args.backend_url,
    )
    while receiver_loop.continue_running:
        receiver_loop._check_for_new_studies()
        receiver_loop.check_for_completed_studies()
        time.sleep(receiver_loop.QUERY_INTERVAL)
