from dcm_classifier.study_processing import ProcessOneDicomStudyToVolumesMappingBase
from dcm_classifier.image_type_inference import ImageTypeClassifierBase
import re
from pydicom import dcmread
from subprocess import run
from typing import Optional
import itk
import json
from pathlib import Path
import datetime
import random

itk.MultiThreaderBase.SetGlobalDefaultNumberOfThreads(1)


def generate_uid():
    """
    Generates a bogus but unique SOP Instance UID for educational or testing purposes.

    Format: [root].[date][time].[random]
        - root: A unique identifier for the organization or project
        - date: Current date in YYYYMMDD format
        - time: Current time in HHMMSS format
        - random: A random number for added uniqueness
    """

    # Define the root UID for your project or organization
    root_uid = "1.2.826.0.1.3680000.9.7411"  # Example root UID

    # Get current date and time
    now = datetime.datetime.now()
    date_str = now.strftime("%Y%m%d")
    time_str = now.strftime("%H%M%S")

    # Generate a random number (in this case, up to 99999 for example)
    random_number = random.randint(1, 99999)

    # Combine elements to form the SOP Instance UID
    sop_instance_uid = f"{root_uid}.{date_str}{time_str}.{random_number}"

    return sop_instance_uid


def write_json_log(
    log_file_path: Path, study_id: str, status: str, reason: Optional[str]
) -> None:
    """
    Writes the current log to the file.
    :param log_file_path: path to the log file
    :param study_id: unique identifier for the study
    :param status: status of the job
    :param reason: reason for the status
    :return: None
    """
    log_entries = {"study_id": study_id, "status": status, "reason": reason}
    # write as json using dump
    with open(log_file_path, "w") as log_file:
        json.dump(log_entries, log_file, indent=4)


def validate_subject_id(subject_id: str) -> str:
    if "sub-" in subject_id:
        return subject_id
    else:
        return f"sub-{subject_id}"


def validate_session_id(session_id: str) -> str:
    if "ses-" in session_id:
        return session_id
    else:
        return f"ses-{session_id}"


def dicom_inference_and_conversion(session_dir: str, output_dir: str) -> str:
    """
    This function takes a session directory with dicom data and converts them to NIfTI files in BIDS format.
    :param session_dir: path to the session directory with dicom data
    :param output_dir: path to the output directory (base NIfTI directory)
    :param model_path: path to the model used for image type inference
    :param dcm2niix_path_path: path to the dcm2niix script
    :return: path to the NIfTI sub-*/ses-* directory with converted data
    """
    inferer = ImageTypeClassifierBase()
    study = ProcessOneDicomStudyToVolumesMappingBase(
        study_directory=session_dir, inferer=inferer
    )
    study.run_inference()
    sub, ses, sub_ses_dir = None, None, None
    for series_number, series in study.series_dictionary.items():
        dcm_info = dcmread(
            series.volume_info_list[0].one_volume_dcm_filenames[0],
            stop_before_pixels=True,
            force=True,
        )
        sub = re.sub("[\W_]", "", dcm_info["PatientID"].value)
        ses = re.sub("[\W_]", "", dcm_info["AcquisitionDate"].value)
        sub_ses_dir = f"{output_dir}/sub-{sub}/ses-{ses}/raw_nifti"
        if not Path(sub_ses_dir).exists():
            run(["mkdir", "-p", sub_ses_dir])

        plane = series.get_acquisition_plane()
        print("Sub:", sub, "series:", series_number, "plane:", plane)

        modality = series.get_series_modality()
        if modality != "INVALID":
            if not Path(sub_ses_dir).exists():
                run(["mkdir", "-p", sub_ses_dir])
            fname = f"{validate_subject_id(sub)}_{validate_session_id(ses)}_acq-{plane}_{modality}"
            series_vol_list = series.get_volume_list()
            if len(series_vol_list) > 1:
                print(
                    f"Series {series_number} not supported. More than one volume in series."
                )
            else:
                itk_im = series_vol_list[0].get_itk_image()
                itk.imwrite(itk_im, f"{sub_ses_dir}/{fname}.nii.gz")

    return sub_ses_dir
