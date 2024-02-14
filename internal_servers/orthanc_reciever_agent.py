import pyorthanc
import time
import subprocess
from pathlib import Path

# Configure PyOrthanc client
orthanc = pyorthanc.Orthanc("http://localhost:8026")  # Adjust the URL as needed


def wait_for_study_to_stabilize(study):
    """
    Wait for the study to stabilize before downloading it.
    """
    # Implement study stabilization logic
    # This might involve checking the study status and waiting for it to become stable
    is_stable: bool = False
    try:
        is_stable = study.get_main_information().get("IsStable", False)
    except Exception as get_main_info_e:
        msg: str = (
            f"ERROR getting study main information for {study.id_}: {get_main_info_e}"
        )
        print(msg)
    return is_stable


def download_study(study_id, download_path):
    """
    Download the study data from Orthanc.
    """
    # Implement study download logic
    # This might involve using PyOrthanc methods to fetch and save DICOM files or other data
    pass  # Placeholder for download logic


def process_data(data_path):
    """
    Call another script to process the downloaded data.
    """
    subprocess.run(["python", "process_data_script.py", data_path], check=True)


def main():
    while True:
        # Fetch list of studies
        studies: list[pyorthanc.Study] = pyorthanc.find_studies()
        for study in studies:
            # TODO : ADD Log HERE
            if wait_for_study_to_stabilize(study):

                # Download study data
                download_path = Path("downloaded_data")
                download_study(study.id_, download_path)
                # Process the downloaded data
                process_data(download_path)
            else:
                print(f"Study {study.id_} is not stable yet. Skipping download.")
        time.sleep(5)


if __name__ == "__main__":
    main()
