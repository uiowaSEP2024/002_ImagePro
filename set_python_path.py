import os
from pathlib import Path

current_directory = Path(__file__).parent
job_monitoring_app_directory = current_directory / "job_monitoring_app"
trackerapi_directory = job_monitoring_app_directory / "trackerapi" / "trackerapi"

# List of directories that contain your modules
directories = [job_monitoring_app_directory, trackerapi_directory, current_directory]

# Get the current PYTHONPATH
python_path = os.environ.get("PYTHONPATH", "").split(os.pathsep)
print("Current PYTHONPATH:", python_path)
# Add your directories to the PYTHONPATH if they are not already there
for directory in directories:
    if directory not in python_path:
        python_path.append(directory.as_posix())

# Update the PYTHONPATH environment variable
os.environ["PYTHONPATH"] = os.pathsep.join(python_path)

# Verify that the directories have been added
print("Updated PYTHONPATH:", os.environ["PYTHONPATH"])
