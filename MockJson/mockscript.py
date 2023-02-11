import uuid
import json
import time

client_id = str(uuid.uuid4())
job_id = str(uuid.uuid4())
client_name = "RandomName"

steps = 20

job_dict = {
    "client_id": client_id,
    "job_id": job_id,
    "client_name": client_name,
}

# print(job_dict)

for i in range(steps):
    time.sleep(3)
    job_dict[i + 1] = "Step " + str(i + 1)

json_object = json.dumps(job_dict, indent=4)

with open("MockJson/sample.json", "w") as outfile:
    outfile.write(json_object)


