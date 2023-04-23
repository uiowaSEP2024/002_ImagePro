import json
import os
import random
import time
import uuid
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from trackerapi import TrackerApi, JobConfigManager

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


# Send request to create the JOB
# Replace with send_event(....)


def run_mock_job(customer_id=None):
    steps = 10
    job_id = generate_uuid()

    # Get job config
    job_configurations_file = Path(SCRIPT_DIR, "./job-configurations.json")
    job_config_manager = JobConfigManager(configurations_file=job_configurations_file)
    job_config = job_config_manager.get_job_config('mockscript_job')

    # Create TrackerAPI object and job session
    tracker = TrackerApi(TRACKER_API_KEY)
    tracker.register_job_config(job_config)

    # Signal the start of a new job TODO: change to use 'tag' instead of name
    job_tracker = tracker.create_job(job_id, customer_id, job_config.name)

    with open(f"{SCRIPT_DIR}/{LOG_FILE_PATH}", "a+") as outfile:
        # Do a dummy job for N steps
        for idx, step in enumerate(job_config.steps):
            # Do some work lasting anywhere between 1-2 seconds
            time.sleep(step.points / 10)

            # Prepare log data
            log_data = {
                "job_id": job_id,
                "customer_id": customer_id,
                "step": step.name,
                "time": str(datetime.now()),
            }

            # sample metadata
            metadata = {
                "Official": "Yes"
            }

            json_str = json.dumps(log_data)

            # Print json to file
            printf(outfile, json_str + "\n")

            # Convenience print to console for live log
            # just so we don't have to sit and wait for file to be logged to
            print(json_str)

            is_last_step = idx == steps - 1
            kind = "complete" if is_last_step else "step"

            job_tracker.send_event(kind, step.name, metadata)


if __name__ == "__main__":
    sample_customer_ids = [
        1,  # johndoe@gmail.com see backend/seed.py
        2,  # janeblack@gmail.com see backend/seed.py
    ]

    # Select a random customer
    random_customer_id = sample_customer_ids[
        random.randrange(0, len(sample_customer_ids))
    ]

    # Run job for the chosen customer
    run_mock_job(customer_id=1)
