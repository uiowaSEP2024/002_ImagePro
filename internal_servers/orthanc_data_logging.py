import json
from typing import List


class OrthancStudyLogger:
    def __init__(self, hospital_id, study_id, log_file_path="medical_image_log.json"):
        self.hospital_id = hospital_id
        self.study_id = study_id
        self.log_file_path = log_file_path
        self.steps = [
            {"step_name": "Data Receiving", "status": "in progress"},
            {"step_name": "Data Download", "status": "incomplete"},
            {"step_name": "Data Processing", "status": "incomplete"},
            {"step_name": "Data Sent to Hospital", "status": "incomplete"},
        ]
        self.internal_product_log = None
        self._write_log()

    def _write_log(self):
        """Writes the current log to the file."""
        log_entries = [{"hospital_id": self.hospital_id, "study_id": self.study_id, **step} for step in self.steps]
        with open(self.log_file_path, 'w') as log_file:
            json.dump(log_entries, log_file, indent=4)

    def update_step_status(self, step_name, status):
        """Updates the status of a given step and re-writes the log file."""
        for step in self.steps:
            if step["step_name"] == step_name:
                step["status"] = status
                break
        self._write_log()

    def mark_step_complete(self, step_name):
        """Marks a given step as complete."""
        self.update_step_status(step_name, "complete")


# Example of using the MedicalImageLogger
logger = MedicalImageLogger(hospital_id="H123", study_id="S456")
logger.mark_step_complete("Data receiving detected")
logger.mark_step_complete("Data stable")
