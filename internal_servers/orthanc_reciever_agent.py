from datetime import datetime

import pyorthanc
import time
import subprocess
from pathlib import Path
from orthanc_data_logging import MedicalImageLogger


def check_study_stable(study: pyorthanc.Study) -> bool:
    """
    Check if the study is stable.

    This function checks if the study is stable by fetching the main information of the study and checking the "IsStable" key.
    param study: The study to check.
    return: True if the study is stable, False otherwise.
    """
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


def map_aet_to_hospital_id(aet: str) -> str:
    """
    Map an AET to a hospital ID.
    This function maps an AET to a hospital ID. This is useful for identifying the hospital that sent a study.
    param aet: The AET to map.
    return: The hospital ID.
    """
    # TODO Implement mapping logic
    return "H123"  # Placeholder for mapping logic


# TODO make the study_processed_dict its own class
def make_list_of_studies_to_process(
    study_processed_dict: dict[str, any], orthanc_client: pyorthanc.Orthanc
) -> list[pyorthanc.Study]:
    """
    Fetch the list of studies to process from Orthanc.
    This function uses PyOrthanc to fetch the list of studies from Orthanc and then filters out invalid studies for a variety of reasons.

    param study_processed_dict: A dictionary of studies that have already been processed.
        The keys are the study IDs and the values are the time the study was processed.
    param orthanc_client: The PyOrthanc client to use to fetch the list of studies.
    return: A list of studies to process.
    """
    studies: list[pyorthanc.Study] = pyorthanc.find_studies(client=orthanc_client)
    # Filter out studies that have already been processed
    studies_to_process = []
    for study in studies:
        study_id = study.id_
        has_properties = False
        if study_id not in study_processed_dict:
            hospital_id = None
            for series in study.series:
                # This is ensures that the study has a series with the description "PROPERTIES" as we will
                # need this in the future to process the study
                if (
                    series.get_main_information()["MainDicomTags"]["SeriesDescription"]
                    == "PROPERTIES"
                ):
                    has_properties = True
                    # TODO Update this to have the hospital_id
                    hospital_id = map_aet_to_hospital_id(
                        series.get_main_information()["MainDicomTags"]["2100-0140"]
                    )

                    break
            # This logic is redundant currently but may be useful in the future
            # The properties files should be created on the first reception of the studies Dicom files
            # The only way to not have properties is if the study was not received correctly
            #
            if has_properties and hospital_id is not None:
                study_processed_dict[study_id] = MedicalImageLogger(
                    hospital_id, study_id
                )
            else:
                print(f"Study {study_id} does not have properties. Skipping..")
                # TODO: Check if we want to delete the study if it does not have properties
                continue
            is_stable = check_study_stable(study)
            if not is_stable:
                print(
                    f"Study {study_id} is not stable yet. Waiting for it to become stable.."
                )
                continue
        else:
            print(f"Study {study_id} has already been processed. Skipping..")
        if not has_properties:
            print(f"Study {study_id} does not have properties. Skipping..")

            continue
        else:
            studies_to_process.append(study)
    return sorted(
        studies_to_process,
        reverse=True,
        key=lambda x: datetime.strptime(
            x.get_main_information()["LastUpdate"], "%Y%m%dT%H%M%S"
        ),
    )


def main():
    with pyorthanc.Orthanc("http://localhost:8026") as internal_orthanc:
        while True:
            study_processed_dict = {}
            # Fetch list of studies
            studies = make_list_of_studies_to_process(
                study_processed_dict, internal_orthanc
            )

            for study in studies:
                # TODO : ADD initial Log HERE

                if check_study_stable(study):
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
