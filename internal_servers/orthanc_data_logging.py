import json
from typing import Optional
from pathlib import Path
from typing import Union
from job-monitoring-app.trackerapi import JobConfigManager, TrackerApi


class OrthancStudyLogger:
    def __init__(self, hospital_id, study_id, tracker_api_key, job_config_file: Union[Path, str]):
        self.hospital_id = hospital_id
        self.study_id = study_id
        self.internal_product_log = None

        # TODO: This is sudo code how to initiate the connection to the tracker api
        # TODO: this will allow us to store data in the database without log files
        # Get job config, use the initial hospital_job.json file
        job_configurations_file = Path(job_config_file)
        job_config_manager = JobConfigManager(configurations_file=job_configurations_file)
        job_config = job_config_manager.get_job_config("hospital_job")

        # Create TrackerAPI object and job session
        tracker = TrackerApi(tracker_api_key)
        tracker.register_job_config(job_config)

        # Signal the start of a new job
        self.tracker_job = tracker.create_job(study_id, hospital_id, job_config.tag)

        # TODO: code below creates the initial events with initial status
        # TODO: we need to change instead of using "kind" fot "step" or "complete" to use the status in event metadata
        # TODO: look in the mockscript to see how they use kind
        self.tracker_job.send_event(
            kind="step",
            tag=0,
            provider_job_id=self.hospital_id,
            metadata={"status": "In Progress"}
        )
        for i in range(1, 4):
            self.tracker_job.send_event(
                kind="step",
                tag=i,
                provider_job_id=self.hospital_id,
                metadata={"status": "Incomplete"}
            )


    def update_step_status(
        self, step_tag: int, status: str, reason: Optional[str] = None
    ):
        """Updates the status of a given step and re-writes the log file."""
        print(f"Updating step {step_tag} to {status}")
        metadata = {"status": status}
        if reason:
            metadata["Reason"] = reason

        # TODO: Update step
        # TODO: this needs to be implemented to allow for updating step in the api and backend
        self.tracker_job.update_event(
                tag=step_tag,
                provider_job_id=self.hospital_id,
                metadata=metadata
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

    def _stage_is_complete(self, stage_id: int) -> bool:
        """Checks if a given stage is complete."""
        stage = self.steps[stage_id - 1]
        return stage["status"] == "complete"

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

        self._write_log()


# Example of using the MedicalImageLogger
logger = OrthancStudyLogger(hospital_id="H123", study_id="S456")
