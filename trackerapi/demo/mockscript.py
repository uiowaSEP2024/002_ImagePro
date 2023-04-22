import json
import os
import random
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from trackerapi.trackerapi import TrackerApi

from demo import job_configuration

load_dotenv()

TEAM3_API_KEY = os.environ.get("TEAM3_API_KEY")

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

    # Create TrackerAPI object

    tracker = TrackerApi("q-jAqPWCRGr2u6SeK6r6U0LBfJA")

    # Create a Job Object

    job_tracker = tracker.register_and_create_job(
        job_id, customer_id, job_configuration.prostate_v1_config
    )

    with open(f"{SCRIPT_DIR}/{LOG_FILE_PATH}", "a+") as outfile:
        # Do a dummy job for N steps
        for i in range(steps):
            # Do some work lasting anywhere between 1-2 seconds
            time.sleep(random.randint(1, 2))

            # Prepare log data
            json_data = {
                "job_id": job_id,
                "customer_id": customer_id,
                "step": "step {}".format(i),
                "time": str(datetime.now()),
            }

            # sample metadata
            metadata = {
                "official": "Yes"
            }

            json_str = json.dumps(json_data)

            # Print json to file
            printf(outfile, json_str + "\n")

            # Convenience print to console for live log
            # just so we don't have to sit and wait for file to be logged to
            print(json_str)

            is_last_step = i == steps - 1
            if is_last_step:
                kind = "complete"
            else:
                kind = "step"

            job_tracker.send_event(kind, "step {}".format(i), metadata)


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
