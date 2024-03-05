import shutil
from datetime import datetime
from pathlib import Path
import pyorthanc
import subprocess
import time
import zipfile
from internal_servers.orthanc_data_logging import OrthancStudyLogger


product_path = Path(__file__).parent / "example_tool" / "brainmask_tool.py"


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


def download_study(study_id, download_dir: str, orthanc: pyorthanc.Orthanc):
    """
    Downloads a DICOM study from an Orthanc server using pyorthanc and saves it to a specified directory as a ZIP file.

    Args:
    - study_id (str): The unique identifier of the DICOM study to be downloaded.
    - download_dir (str): The directory path where the ZIP file will be saved.
    - orthanc (pyorthanc.Orthanc): The Orthanc server object.

    This function first attempts to download the entire DICOM study associated with the given
    study_id from the Orthanc server in ZIP format using the pyorthanc client. If the download is successful,
    the ZIP file is saved to the specified directory. If the directory does not exist, it is created.

    The function prints a message indicating the success or failure of the download operation.
    """
    # Ensure the Path object is used for path operations
    download_dir = Path(download_dir)
    download_dir.mkdir(
        parents=True, exist_ok=True
    )  # Ensure the download directory exists

    # Define the path for the ZIP file
    zip_path = download_dir / f"{study_id}.zip"

    try:
        # Use pyorthanc to download the study as a ZIP archive
        study_archive = orthanc.get_studies_id_archive(study_id)

        # Save the ZIP file to the specified path
        with open(zip_path, "wb") as f:
            f.write(study_archive)
        print(f"Downloaded and saved DICOM study ZIP to {zip_path}")
        return zip_path
    except Exception as e:
        print(f"Error to download DICOM study for study ID {study_id}. Error: {e}")


def unzip_study(zip_path: str, extract_dir: str):
    """
    Extracts a ZIP file containing a DICOM study into a specified directory.

    Args:
    - zip_path (str): The path to the ZIP file to be extracted.
    - extract_dir (str): The directory path where the contents of the ZIP file will be extracted.

    This function attempts to extract all the contents of the ZIP file specified by zip_path
    into the directory specified by extract_dir. If the directory does not exist, it is created.

    The function prints a message indicating the success or failure of the extraction operation.
    """

    # Ensure the Path objects are used for path operations
    zip_path = Path(zip_path)
    extract_dir = Path(extract_dir)
    extract_dir.mkdir(
        parents=True, exist_ok=True
    )  # Ensure the extraction directory exists

    try:
        # Open the ZIP file and extract its contents
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
        print(f"Extracted DICOM study to {extract_dir}")
    except Exception as e:
        print(f"Error to extract ZIP file {zip_path}. Error: {e}")


def process_data(
    brains_tool_path: str, study_id: str, input_data_path: str, output_path: str
):
    """
    Runs a Python script to process DICOM data using subprocess, with specified paths for the script, input data, and output.

    Args:
    - brains_tool_path (str): The full path to the brainmask_tool.py script.
    - study_id (str): Study id for the study being processed.
    - input_data_path (str): The directory path where the input DICOM data is located.
    - output_path (str): The directory path where the processed data will be saved.

    This function executes the brainmask_tool.py script with specified input and output directories
    using subprocess.run. It checks for execution success and prints the script output or errors.
    """

    # Ensure the output directory exists
    Path(output_path).mkdir(parents=True, exist_ok=True)

    # Command to run the script
    command = [
        "python3",
        brains_tool_path,
        "-i",
        study_id,
        "-s",
        input_data_path,
        "-o",
        output_path,
    ]

    try:
        # Execute the command
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(f"Script output: {result.stdout}")
        print("Script executed successfully.")
    except Exception as e:
        print(f"Error executing script: {e}")


def upload_data_to_internal(directory_path: str, orthanc: pyorthanc.Orthanc):
    """
    Uploads DICOM files from a specified directory back to an Orthanc server.

    Args:
    - directory_path (str): The path to the directory containing DICOM files to be uploaded.
    - orthanc (pyorthanc.Orthanc): The Orthanc server object.
    """
    # Iterate over each file in the directory and upload it
    directory = Path(directory_path)
    for file_path in directory.rglob(
        "*.dcm"
    ):  # Assuming DICOM files have .dcm extension
        try:
            with open(file_path, "rb") as file:
                result = orthanc.post_instances(file.read())
                print(result.get("Status"))
                print(result)
            print(f"Successfully uploaded {file_path.name} to Orthanc.")
        except Exception as e:
            print(f"Failed to upload {file_path.name}. Error: {e}")


def return_to_original_hospital(orthanc: pyorthanc.Orthanc, study_id: str):
    """
    Return data to the original sender - Hospital PACS

    Args:
    - orthanc (pyorthanc.Orthanc): The Orthanc server object.
    - study_id (str): Study id for the study being processed.
    """
    response = orthanc.post_modalities_id_store("EXAMPLE_HOSPITAL_NAME", data={"study_id": study_id})
    print(response)


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
                    study_config_file="hospital_job_configuration.json",
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


def main(internal_data_path: Path):
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
                            study_data_path = internal_data_path / study.id_
                            zip_path = download_study(
                                study.id_,
                                f"{study_data_path}/archive",
                                internal_orthanc,
                            )
                            unzip_study(zip_path.as_posix(), f"{study_data_path}/data")
                            current_logger.update_step_status(2, "Complete")
                        except Exception as e:
                            current_logger.update_step_status(2, "Error", str(e))
                    if current_logger.step_is_ready(3):
                        current_logger.update_step_status(3, "In progress")
                        try:
                            process_data(
                                brains_tool_path=product_path.as_posix(),
                                study_id=study.id_,
                                input_data_path=f"{study_data_path}/data",
                                output_path=f"{study_data_path}/results",
                            )
                            # TODO Update this to have the processed data path
                            current_logger.update_step_status(3, "Complete")
                            # current_logger.update_data_processing("download_path")
                        except Exception as e:
                            current_logger.update_step_status(3, "Error", str(e))
                    if current_logger.step_is_ready(4):
                        current_logger.update_step_status(4, "In progress")
                        try:
                            upload_data_to_internal(
                                directory_path=f"{study_data_path}/deliverables",
                                orthanc=internal_orthanc,
                            )
                            return_to_original_hospital(internal_orthanc, study.id_)
                            current_logger.update_step_status(4, "Complete")
                        except Exception as e:
                            current_logger.update_step_status(4, "Error", str(e))

                    if current_logger._stage_is_complete(4):
                        print(
                            f"Study {study.id_} has been processed and sent to hospital"
                        )

                        print(f"Deleting study {study.id_}")
                        # delete the study from the internal orthanc
                        internal_orthanc.delete_studies_id(study.id_)
                        study_processed_dict.pop(study.id_)
                        # delete study from local system
                        shutil.rmtree(study_data_path)

            print("Sleeping for 10 seconds..")
            time.sleep(10)


if __name__ == "__main__":
    main(Path("/home/mbrzus/programming/002_ImagePro/example_tool/example_output"))
