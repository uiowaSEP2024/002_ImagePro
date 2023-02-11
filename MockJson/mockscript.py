import uuid
import json
import time

client_id = str(uuid.uuid4())
job_id = str(uuid.uuid4())
client_name = "RandomName"

steps = 20
json_begin = '{"objects":[\n'
json_end = ']}'

with open("MockJson/sample.json", "w") as outfile:
    outfile.write(json_begin)
    for i in range(steps):
        time.sleep(3)
        json_object = json.dumps(
            {
                "client_id": client_id,
                "job_id": job_id,
                "client_name": client_name,
                "step": i+1 
            },
            indent=4,
            # separators=(',',': ')
        )
        outfile.write(json_object)
        if i != (steps - 1):  
            outfile.write(",")
        outfile.write("\n")
    
    outfile.write(json_end)
        
