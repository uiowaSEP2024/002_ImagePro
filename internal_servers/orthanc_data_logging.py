import json
from typing import Optional
from pathlib import Path
from typing import Union
from job_monitoring_app.trackerapi.trackerapi import TrackerApi, StudyConfigManager
import os

from dotenv import load_dotenv

base_project_dir = Path(__file__).parent.parent
relative_env_path = base_project_dir / "job_monitoring_app/backend/.env.local"
assert relative_env_path.exists(), f"Expected to find .env file at {relative_env_path}"
load_dotenv(relative_env_path)

API_KEY = os.environ.get("API_KEY")


class OrthancStudyLogger:
    def __init__(
        self,
        hospital_id,
        study_id,
        tracker_api_key,
        study_config_file: Union[Path, str],
    ):
        self.hospital_id = (
            hospital_id  # hospital_id corresponds to the customer_id in the backend
        )
        self.study_id = (
            study_id  # study_id corresponds to the provider_study_id in the backend
        )
        self.internal_product_log = None

        # Get study config, use the initial hospital_study.json file
        study_configurations_file = Path(study_config_file)
        study_config_manager = StudyConfigManager(
            configurations_file=study_configurations_file
        )
        study_config = study_config_manager.get_study_config("hospital_study")

        # Create TrackerAPI object and study session
        tracker = TrackerApi(tracker_api_key)
        tracker.register_study_config(study_config)

        # Signal the start of a new study
        self.tracker_study = tracker.create_study(
            study_id, hospital_id, study_config.tag
        )

        self.steps = {
            1: {"status": "Pending"},
            2: {"status": "Pending"},
            3: {"status": "Pending"},
            4: {"status": "Pending"},
        }

        # These are the primary keys for each event logged in the back end
        self.step_PKs = {}

        for idx, step in enumerate(study_config.step_configurations):
            new_event = self.tracker_study.send_event(
                kind="Pending",
                tag=step.tag,
                metadata=self.steps[
                    idx + 1
                ],  # this will take the initial metadata from self.steps
            )
            # Log the ID of each event
            self.step_PKs[idx + 1] = new_event.event_id

        # # mock pipeline
        # for step in self.step_PKs:
        #     time.sleep(5)
        #     self.update_step_status(step, "In progress")
        #     time.sleep(5)
        #     self.update_step_status(step, "Complete")

    def update_step_status(
        self, step_id: int, status: str, reason: Optional[str] = None
    ):
        """
        Updates the status of a given step and re-writes the log file.
        """
        print(f"Updating step {step_id} to {status}")
        metadata = {"status": status}
        self.steps[step_id] = {"status": status}
        if reason:
            metadata["Reason"] = reason

        # event_id becomes the primary key of the event corresponding to this event for this study
        # it is saved in self.step_PKs
        self.tracker_study.update_event(
            kind=status, event_id=self.step_PKs[step_id], metadata=metadata
        )

    def step_is_ready(self, step_id: int) -> bool:
        """Checks if a given step is ready to begin."""
        previous_steps = []
        for i in range(1, step_id):
            previous_steps.append(self.steps[i])
        is_ready = True
        for step in previous_steps:
            if step["status"] != "Complete":
                is_ready = False
                break
        return is_ready

    def _stage_is_complete(self, step_id: int) -> bool:
        """Checks if a given stage is complete."""
        status = self.steps[step_id]["status"]
        return status == "Complete"

    def update_data_processing(self, log_file_path: str):
        """
        Updates the status of data processing based on product produced log file.
        The log file should be a json file with the following format:
        {
            "status": "complete/failed"
            "reason": "optional message"
        }
        If the status is failed, the reason should be included.

        If the status is complete, the data processing step is marked as complete.
        """
        with open(log_file_path, "r") as log_file:
            self.internal_product_log = json.load(log_file)
        if self.internal_product_log["status"] == "Complete":
            self.update_step_status(3, "Complete")
        else:
            self.update_step_status(
                3, "Error", reason=self.internal_product_log["reason"]
            )


# Example of using the MedicalImageLogger
if __name__ == "__main__":
    logger = OrthancStudyLogger(
        hospital_id=1,
        study_id=433,
        tracker_api_key=API_KEY,
        study_config_file="hospital_study_configuration.json",
    )

# Note: the tracker_api_key needs to be replaced by creating a provider account on the app
# and generating an api key for your account and pasting that in the OrthancStudyLogger above
