import json
import os
import random
import time
import uuid
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from trackerapi import StudyConfigManager, TrackerApi

load_dotenv()

TRACKER_API_KEY = os.environ.get("TRACKER_API_KEY")
LOG_FILE_PATH = "logs.txt"
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def generate_uuid():
    # Create a random uuid
    return str(uuid.uuid4())


def printf(file, data):
    # Write the data to a file
    file.write(data)


# Send request to create the Study
# Replace with send_event(....)


def run_mock_study(customer_id=None):
    steps = 10
    study_id = generate_uuid()

    # Get study config
    study_configurations_file = Path(SCRIPT_DIR, "study-configurations.json")
    study_config_manager = StudyConfigManager(
        configurations_file=study_configurations_file
    )
    study_config = study_config_manager.get_study_config("mockscript_study")

    # Create TrackerAPI object and study session
    tracker = TrackerApi(TRACKER_API_KEY)
    tracker.register_study_config(study_config)

    # Signal the start of a new study
    tracker_study = tracker.create_study(study_id, customer_id, study_config.tag)

    with open(f"{SCRIPT_DIR}/{LOG_FILE_PATH}", "a+") as outfile:
        # Do a dummy study for N steps
        for idx, step in enumerate(study_config.step_configurations):
            # Do some work lasting anywhere between 1-2 seconds
            time.sleep(step.points / 10)

            step_time = str(datetime.now())
            # Prepare log data
            log_data = {
                "study_id": study_id,
                "customer_id": customer_id,
                "step": step.name,
                "time": step_time,
            }

            # sample metadata
            metadata = {"Certified": "Yes", "Duration": f"{step.points/10}s"}

            json_str = json.dumps(log_data)

            # Print json to file
            printf(outfile, json_str + "\n")

            # Convenience print to console for live log
            # just so we don't have to sit and wait for file to be logged to
            print(json_str)

            is_last_step = idx == steps - 1
            kind = "complete" if is_last_step else "step"

            tracker_study.send_event(kind, step.tag, metadata)


if __name__ == "__main__":
    sample_customer_ids = [
        1,  # johndoe@gmail.com see backend/seed.py
        2,  # janeblack@gmail.com see backend/seed.py
    ]

    # Select a random customer
    random_customer_id = sample_customer_ids[
        random.randrange(0, len(sample_customer_ids))
    ]

    # Run study for the chosen customer
    run_mock_study(customer_id=1)
