import json
from typing import Optional
from pathlib import Path
from typing import Union
from job_monitoring_app.trackerapi.trackerapi import TrackerApi, JobConfigManager


class OrthancStudyLogger:
    def __init__(
        self, hospital_id, study_id, tracker_api_key, job_config_file: Union[Path, str]
    ):
        self.hospital_id = hospital_id
        self.study_id = study_id
        self.internal_product_log = None

        # TODO: This is sudo code how to initiate the connection to the tracker api
        # TODO: this will allow us to store data in the database without log files
        # Get job config, use the initial hospital_job.json file
        job_configurations_file = Path(job_config_file)
        job_config_manager = JobConfigManager(
            configurations_file=job_configurations_file
        )
        job_config = job_config_manager.get_job_config("hospital_job")

        # Create TrackerAPI object and job session
        tracker = TrackerApi(tracker_api_key)
        tracker.register_job_config(job_config)

        # Signal the start of a new job
        self.tracker_job = tracker.create_job(study_id, hospital_id, job_config.tag)
        # job_config = None
        # TODO: the steps are used to check if step is complete for the orthanc receiver
        self.steps = {
            1: {"status": "In Progress"},
            2: {"status": "Incomplete"},
            3: {"status": "Incomplete"},
            4: {"status": "Incomplete"},
        }

        # TODO: code below creates the initial events with initial status
        # TODO: we need to change instead of using "kind" fot "step" or "complete" to use the status in event metadata
        # TODO: look in the mockscript to see how they use kind
        # for i in range(1, 5):
        #     self.tracker_job.send_event(
        #         kind="step",
        #         tag=i,
        #         provider_job_id=self.hospital_id,
        #         metadata=self.steps[i], # this will take the initial metadata from self.steps
        #     )

        # These are the primary keys for each event logged in the back end
        self.event_ids = {}

        for idx, step in enumerate(job_config.step_configurations):
            new_event = self.tracker_job.send_event(
                kind="step",
                tag=step.tag,
                # provider_job_id=self.hospital_id,
                metadata=self.steps[
                    idx + 1
                ],  # this will take the initial metadata from self.steps
            )
            # Log the ID of each event
            self.event_ids[idx + 1] = new_event.event_id

    def update_step_status(
        self, step_id: int, status: str, reason: Optional[str] = None
    ):
        """Updates the status of a given step and re-writes the log file."""
        print(f"Updating step {step_id} to {status}")
        metadata = {"status": status}
        self.steps[step_id] = {"status": status}
        if reason:
            metadata["Reason"] = reason

        # TODO: Update step
        # TODO: this needs to be implemented to allow for updating step in the api and backend
        # event_id becomes the primary key of the event corresponding to this event for this job, which is saved in self.event_ids
        self.tracker_job.update_event(
            kind=status, event_id=self.event_ids[step_id], metadata=metadata
        )

    def step_is_ready(self, step_id: int) -> bool:
        """Checks if a given step is ready to begin."""
        previous_steps = self.steps[: step_id - 1]
        is_ready = True
        for step in previous_steps:
            if step["status"] != "complete":
                is_ready = False
                break
        return is_ready

    def _stage_is_complete(self, step_tag: int) -> bool:
        """Checks if a given stage is complete."""
        # TODO: I had to update this. It is not tested and might be buggy
        status = self.steps[step_tag]["status"]
        return status == "complete"

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
        if self.internal_product_log["status"] == "complete":
            self.update_step_status(3, "complete")
        else:
            self.update_step_status(
                3, "failed", reason=self.internal_product_log["reason"]
            )


# Example of using the MedicalImageLogger
if __name__ == "__main__":
    logger = OrthancStudyLogger(
        hospital_id=1,
        study_id=1000,
        tracker_api_key="34faWJnoajfaxrpIDqwasxAW_KU",
        job_config_file="hospital_job_configuration.json",
    )
    # logger.update_step_status(1, "complete")
    # logger.update_step_status(2, "complete")
    # logger.update_step_status(3, "complete")
    # logger.update_step_status(4, "complete")
# Note: the tracker_api_key needs to be replaced by creating a provider account on the app
# and generating an api key for your account and pasting that in the OrthancStudyLogger above
