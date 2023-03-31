import os
import uuid
import json
import time
from datetime import datetime
import random

from dotenv import load_dotenv
import requests

load_dotenv()

TEAM3_API_KEY = os.environ.get('TEAM3_API_KEY')

LOG_FILE_PATH = "logs.txt"


def generate_uuid():
    # Create a random uuid
    return str(uuid.uuid4())


def printf(file, data):
    # Write the data to a file
    file.write(data)


# Send request to create the JOB
# Replace with send_event(....)

def run_mock_job(customer_id=None):
    steps = 20
    job_id = generate_uuid()

    # Send request to create job
    create_job_response = requests.post('http://localhost:8000/jobs',
                                        json={
                                            "provider_job_id": job_id,
                                            "customer_id": customer_id,
                                            "provider_job_name": "MockscriptJob"
                                        },
                                        headers={"x-api_key": TEAM3_API_KEY}
                                        )

    if create_job_response.status_code != 200:
        raise Exception("Failed to initialize job with service!")

    with open(LOG_FILE_PATH, "a+") as outfile:
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

            json_str = json.dumps(json_data)

            # Print json to file
            # printf(outfile, json_str + "\n")

            # Convenience print to console for live log
            # just so we don't have to sit and wait for file to be logged to
            print(json_str)

            is_last_step = i == steps - 1
            if is_last_step:
                kind = 'complete'
            else:
                kind = 'step'

            requests.post('http://localhost:8000/events',
                          json={
                              "kind": kind,
                              "name": "step {}".format(i),
                              "provider_job_id": job_id
                          },
                          headers={"x-api_key": TEAM3_API_KEY}
                          )


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
    run_mock_job(customer_id=random_customer_id)
