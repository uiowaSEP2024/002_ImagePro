from datetime import datetime
from pathlib import Path
import pyorthanc
import time
from internal_servers.orthanc_data_logging import OrthancStudyLogger


def check_study_stable(study: pyorthanc.Study) -> bool:
    """
    Check if the study is stable.

    This function checks if the study is stable by fetching the main information
    of the study and checking the "IsStable" key.
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
    pass
    # subprocess.run(["python", "process_data_script.py", data_path], check=True)


def send_data_to_hospital(data_path, hospital_id):
    """
    Send the processed data to the hospital.
    """
    pass  # Placeholder for sending data to hospital logic


def map_aet_to_hospital_id(aet: str) -> str:
    """
    Map an AET to a hospital ID.
    This function maps an AET to a hospital ID. This is useful for identifying the hospital that sent a study.
    param aet: The AET to map.
    return: The hospital ID.
    """
    # TODO Implement mapping logic
    return "H123"  # Placeholder for mapping logic


def get_default_output_path():
    """
    Get the default output path for the agent.
    This function gets the default output path for the agent. This is useful for identifying where to save logs and
    other files.
    return: The default output path.
    """
    # TODO Replace this with the actual default output path logic or move to agent configuration
    file_loc: Path = Path(__file__)
    example_tool_dir: Path = file_loc.parent.parent / "example_tool"
    output_path: Path = example_tool_dir / "example_output"
    return output_path  # Placeholder for default output path logic


# TODO make the study_processed_dict its own class
def make_list_of_studies_to_process(
    study_processed_dict: dict[str, any], orthanc_client: pyorthanc.Orthanc
) -> list[pyorthanc.Study]:
    """
    Fetch the list of studies to process from Orthanc.
    This function uses PyOrthanc to fetch the list of studies from Orthanc and then filters out invalid studies for a
    variety of reasons.

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
                    # TODO Look into Orthanc Logic to see if we can get the hospital_id from the study
                    # https://orthanc.uclouvain.be/book/plugins/python.html
                    # aet = series.get_main_information()["MainDicomTags"]["2100-0140"]
                    aet = "ExampleAET"
                    hospital_id = map_aet_to_hospital_id(aet)

                    break
            # This logic is redundant currently but may be useful in the future
            # The properties files should be created on the first reception of the studies Dicom files
            # The only way to not have properties is if the study was not received correctly
            #
            if has_properties and hospital_id is not None:
                # output_path = get_default_output_path()
                # log_file_path = output_path / f"{hospital_id}_{study_id}_log.json"
                study_processed_dict[study_id] = OrthancStudyLogger(
                    hospital_id=1,
                    study_id=1,
                    tracker_api_key="34faWJnoajfaxrpIDqwasxAW_KU",
                    job_config_file="hospital_job_configuration.json",
                )
            else:
                print(f"Study {study_id} does not have properties. Skipping..")
                # TODO: Check if we want to delete the study if it does not have properties
                continue
            is_stable = check_study_stable(study)
            if not is_stable:
                # TODO Check if this logic is desired here or if it should be moved to the main loop as its own stage
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
            print(f"Found {len(studies)} studies to process")

            for study in studies:
                current_logger = study_processed_dict[study.id_]
                if check_study_stable(study):
                    current_logger.update_step_status(1, "Complete")
                if current_logger.step_is_ready(2):
                    current_logger.update_step_status(2, "In progress")
                    try:
                        download_study(study.id_, "download_path")
                        current_logger.update_step_status(2, "Complete")
                    except Exception as e:
                        current_logger.update_step_status(2, "Error", str(e))
                if current_logger.step_is_ready(3):
                    current_logger.update_step_status(3, "In progress")
                    try:
                        process_data("download_path")
                        # TODO Update this to have the processed data path
                        current_logger.update_step_status(3, "Complete")
                        # current_logger.update_data_processing("download_path")
                    except Exception as e:
                        current_logger.update_step_status(3, "Error", str(e))
                if current_logger.step_is_ready(4):
                    current_logger.update_step_status(4, "In progress")
                    try:
                        send_data_to_hospital(
                            "processed_data_path", current_logger.hospital_id
                        )
                        current_logger.update_step_status(4, "Complete")
                    except Exception as e:
                        current_logger.update_step_status(4, "Error", str(e))

                if current_logger._stage_is_complete(4):
                    print(f"Study {study.id_} has been processed and sent to hospital")
                    print(f"Deleting study {study.id_}")
                    internal_orthanc.delete_studies_id(study.id_)
                    study_processed_dict.pop(study.id_)

            print("Sleeping for 10 seconds..")
            time.sleep(10)


if __name__ == "__main__":
    main()
