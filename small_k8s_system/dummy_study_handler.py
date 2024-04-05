import time
from kubernetes import client, config
import os


def create_job_with_dynamic_args(api_instance, job_name, image, command, args):
    print("Creating the job with dynamic arguments...")
    job_manifest = {
        "apiVersion": "batch/v1",
        "kind": "Job",
        "metadata": {"name": job_name},
        "spec": {
            "template": {
                "spec": {
                    "containers": [{
                        "name": job_name,
                        "image": image,
                        "command": command,
                        "args": args,
                        "volumeMounts": [{
                            "name": "data-volume",
                            "mountPath": "/data"
                        }]
                    }],
                    "restartPolicy": "Never",
                    "volumes": [{
                        "name": "data-volume",
                        "persistentVolumeClaim": {
                            "claimName": "data-pvc"
                        }
                    }]
                }
            }
        }
    }

    api_response = api_instance.create_namespaced_job(body=job_manifest, namespace="default")
    print(f"Job '{api_response.metadata.name}' created.")


def check_job_completion(api_instance, job_name):
    print("Checking job completion status...")
    completed = False
    while not completed:
        res = api_instance.read_namespaced_job_status(name=job_name, namespace="default")
        if res.status.succeeded:
            print("Job completed successfully.")
            completed = True
        elif res.status.failed:
            print("Job failed.")
            completed = True
        else:
            print("Job still running. Checking again in 5 seconds...")
            time.sleep(5)
    return completed


def main():
    config.load_kube_config()  # Use load_incluster_config() if inside a cluster
    batch_v1 = client.BatchV1Api()

    # Simulate loading data to PVC (Assume it's already done)
    print("Assuming data is already loaded into the PVC...")

    # Wait for 5 seconds
    print("Waiting for 5 seconds before triggering the job...")
    time.sleep(5)

    # Trigger the BrainMask Tool job with dynamic arguments
    job_name = "brainmask-tool-job"
    image = "your-brainmask-tool-image"
    command = ["python", "brainmask_tool.py"]
    args = ["-i", "abc123", "-s", "/data/input", "-o", "/data/output"]
    create_job_with_dynamic_args(batch_v1, job_name, image, command, args)

    # Check for job completion
    if check_job_completion(batch_v1, job_name):
        # Assuming we can access the filesystem where the output is stored (this may need adjustment in real scenarios)
        output_dir = "/data/output"  # Adjust this path based on how your environment is set up
        if os.listdir(output_dir):
            print("Success: Output data found in the PVC.")
        else:
            print("Failure: No output data found in the PVC.")


if __name__ == '__main__':
    main()
