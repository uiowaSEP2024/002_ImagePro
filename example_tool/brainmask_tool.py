#!/usr/bin/env python3
import sys
import argparse

import pydicom
from pdf2dcm import Pdf2EncapsDCM
from subprocess import run
from pipeline_functions import dicom_inference_and_conversion, brainmask_inference, write_json_log
from pdf_report import generate_report
from pydicom import dcmread
from pathlib import Path


description = "author: Michal Brzus\nBrainmask Tool\n"

# parse command line
parser = argparse.ArgumentParser(description=description)
parser.add_argument(
    "-i",
    "--study_id",
    required=True,
    help="Unique identifier for the study",
)
parser.add_argument(
    "-s",
    "--session_dir",
    metavar="directory",
    required=True,
    help="Input dicom session directory",
)
parser.add_argument(
    "-o",
    "--output_dir",
    metavar="directory",
    required=True,
    help="Output nifti directory",
)

if len(sys.argv) == 1:
    parser.print_help()
    exit(1)
args = parser.parse_args()

# setup
session_path = Path(args.session_dir)
output_path = Path(args.output_dir)
study_id = args.study_id
status = None
reason = None
log_file_path = output_path / f"{study_id}_log.json"
current_dir = Path(__file__).parent

stage_name = "Input Data Validation and Conversion"
print(f"Running stage: {stage_name}")
# create output directory
if not Path(args.output_dir).exists():
    print("Creating output directory")
    run(["mkdir", "-p", args.output_dir])

# run dicom inference and NIfTI conversion
print("Processing DICOM data")

try:
    nifti_path = dicom_inference_and_conversion(
        session_dir=session_path.as_posix(),
        output_dir=output_path.as_posix(),
        model_path=f"{current_dir.as_posix()}/rf_dicom_modality_classifier.onnx",
    )
except Exception as e:
    reason = f"Error in stage: {stage_name}"
    status = "failed"
    write_json_log(log_file_path, study_id, status, reason)
    print(reason)
    print(e)
    sys.exit(1)

print("NIfTI files created")
print(f"Successfully finished stage: {stage_name}")

stage_name = "Brainmask Computation"
print(f"Running stage: {stage_name}")
# get NIfTI files
raw_anat_nifti_files = list(Path(nifti_path).glob("*.nii.gz"))

# create data dictionary for inference
data_dict = [{"image": str(f)} for f in raw_anat_nifti_files]

# create output directory for brainmasks
brainmask_output_dir = Path(nifti_path).parent.as_posix() + "/brainmasks"
if not Path(brainmask_output_dir).exists():
    print("Creating brainmask output directory")
    run(["mkdir", "-p", brainmask_output_dir])

# run inference
try:
    print("Running brainmask inference")
    brainmask_inference(data_dict, f"{current_dir.as_posix()}/brainmask_model.ckpt", brainmask_output_dir)
except Exception as e:
    reason = f"Error in stage: {stage_name}"
    status = "failed"
    write_json_log(log_file_path, study_id, status, reason)
    print(reason)
    print(e)
    sys.exit(1)
# create output directory for report
report_output_dir = Path(nifti_path).parent.as_posix() + "/report"
if not Path(report_output_dir).exists():
    print("Creating report output directory")
    run(["mkdir", "-p", report_output_dir])

# make deliverables directory
deliverables_dir = Path(output_path).parent.as_posix() + "/deliverables"
if not Path(deliverables_dir).exists():
    print("Creating report output directory")
    run(["mkdir", "-p", deliverables_dir])


# generate report
stage_name = "Report Generation"
print(f"Running stage: {stage_name}")
im_path = raw_anat_nifti_files[0]
mask_path = list(Path(brainmask_output_dir).glob("*.nii.gz"))[0]
try:
    pdf_fn = generate_report(
        im_path.as_posix(), mask_path.as_posix(), report_output_dir
    )
    print(f"Report created: {pdf_fn}")
except Exception as e:
    reason = f"Error in stage: {stage_name}"
    status = "failed"
    write_json_log(log_file_path, study_id, status, reason)
    print(reason)
    print(e)
    sys.exit(1)


stage_name = "PDF to DICOM conversion"
# This assumes that the template IMA file is in the session directory and that the first .dcm file is the valid
template_dcm = sorted(session_path.rglob("*.dcm"))[0]
print(f"template_dcm: {template_dcm}")
try:
    converter = Pdf2EncapsDCM()
    converted_dcm = converter.run(
        path_pdf=pdf_fn, path_template_dcm=template_dcm.as_posix(), suffix=".dcm"
    )[0]
    del report_output_dir, brainmask_output_dir, nifti_path

    print(f"Report created: {converted_dcm}")

    # Adding needed metadata to the report
    """"""
    pdf_dcm = dcmread(converted_dcm, stop_before_pixels=True)
    template_dcm = dcmread(template_dcm, stop_before_pixels=True)
    for tag in [0x00200010, 0x0020000d, 0x0020000e, 0x00080018, 0x00020000]:
        print(tag)
        data_elem = template_dcm.get(tag)
        if tag == 0x00080018:
            data_elem.value = "1.2.840.10008.1234567890"
        print(data_elem)
        pdf_dcm.add(data_elem)

    pdf_dcm.SeriesDescription = "This is a rough brainmask"
    pdf_dcm.DocumentTitle = f"BrainyBarrier PDF Results"
    pdf_dcm.save_as(converted_dcm, write_like_original=False)

    # move the report.dcm to the deliverables directory
    run(["mv", converted_dcm, f"{deliverables_dir}/"])

except Exception as e:
    reason = f"Error in stage: {stage_name}"
    status = "failed"
    write_json_log(log_file_path, study_id, status, reason)
    print(reason)
    print(e)
    sys.exit(1)

status = "Completed"
write_json_log(log_file_path, study_id, status, reason)
print(f"Successfully finished stage: {stage_name}")

# [ 'tests/test_data/test_file.dcm' ]
