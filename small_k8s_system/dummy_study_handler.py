import time
from kubernetes import client, config
import os
import shutil


def copy_test_data_to_pvc():
    src_dir = "/app/test_data"
    dest_dir = "/data/input"  # Assuming this is the mount path of the PVC
    os.makedirs(dest_dir, exist_ok=True)
    try:
        if os.path.exists(src_dir):
            print(f"Directory {src_dir} exists!")
            # Printing contents of the src_dir
            print("Contents of the source directory:")
            for item in os.listdir(src_dir):
                print(item)

            # Copy the entire directory tree to the destination
            shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)
            print(f"Copied test data from {src_dir} to {dest_dir}")
        else:
            print("Source directory does not exist.")
    except Exception as e:
        print(f"Failed to copy data: {str(e)}")


def create_job_with_dynamic_args(api_instance, job_name, image, command, args):
    print("Creating the job with dynamic arguments...")
    job_manifest = {
        "apiVersion": "batch/v1",
        "kind": "Job",
        "metadata": {"name": job_name, "namespace": "default"},
        "spec": {
            "template": {
                "spec": {
                    "containers": [
                        {
                            "name": job_name,
                            "image": image,
                            "command": command,
                            "args": args,
                            "volumeMounts": [
                                {"name": "data-volume", "mountPath": "/data"}
                            ],
                        }
                    ],
                    "restartPolicy": "Never",
                    "volumes": [
                        {
                            "name": "data-volume",
                            "persistentVolumeClaim": {"claimName": "data-pvc"},
                        }
                    ],
                }
            }
        },
    }

    api_response = api_instance.create_namespaced_job(
        body=job_manifest, namespace="default"
    )
    print(f"Job '{api_response.metadata.name}' created.")
    # Wait a few seconds after job creation before returning
    time.sleep(5)  # Adjust time based on observed API behavior


def check_job_completion(api_instance, job_name):
    print("Checking job completion status...")
    completed = False
    while not completed:
        try:
            res = api_instance.read_namespaced_job_status(job_name, "default")
            if res.status.succeeded == 1:
                print("Job completed successfully.")
                completed = True
            elif res.status.failed is not None and res.status.failed > 0:
                print("Job failed.")
                completed = True
            else:
                print("Job still running. Checking again in 5 seconds...")
                time.sleep(15)
        except client.exceptions.ApiException as e:
            print(f"Error checking job status: {e}")
            break
    return completed


def main():
    try:
        # Use in-cluster configuration if running inside a pod
        config.load_incluster_config()
    except config.ConfigException:
        # Use kubeconfig file if running outside the cluster (e.g., for local debugging)
        config.load_kube_config()
    batch_v1 = client.BatchV1Api()

    # Simulate loading data to PVC (Assume it's already done)
    print("loaded into the PVC...")
    copy_test_data_to_pvc()

    # Wait for 5 seconds
    print("Waiting for 5 seconds before triggering the job...")
    time.sleep(5)

    # Trigger the BrainMask Tool job with dynamic arguments
    job_name = "brainmask-tool-job"
    image = "brainmasktool_light:v0.1"
    command = ["python", "brainmask_tool.py"]
    args = ["-i", "abc123", "-s", "/data/input", "-o", "/data/output"]
    create_job_with_dynamic_args(batch_v1, job_name, image, command, args)

    # Check for job completion
    if check_job_completion(batch_v1, job_name):
        # Assuming we can access the filesystem where the output is stored (this may need adjustment in real scenarios)
        output_dir = (
            "/data/output"  # Adjust this path based on how your environment is set up
        )
        if os.listdir(output_dir):
            print("Success: Output data found in the PVC.")
        else:
            print("Failure: No output data found in the PVC.")


if __name__ == "__main__":
    main()
