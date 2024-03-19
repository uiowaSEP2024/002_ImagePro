#!/usr/bin/env python3
import sys
import argparse
import datetime
from pdf2dcm import Pdf2EncapsDCM
from subprocess import run
from pipeline_functions import dicom_inference_and_conversion, write_json_log, generate_uid
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

# create output directory for report
report_output_dir = Path(nifti_path).parent.as_posix() + "/report"
if not Path(report_output_dir).exists():
    print("Creating report output directory")
    run(["mkdir", "-p", report_output_dir])

# make deliverables directory
deliverables_dir = Path(output_path).parent / "deliverables"
deliverables_dir.mkdir(parents=True, exist_ok=True)

# generate report
stage_name = "Report Generation"
print(f"Running stage: {stage_name}")
try:
    pdf_fn = generate_report(
        report_output_dir
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
# This assumes that the template IMA file is in the session directory and that the first IAM file is the valid
try:
    template_dcm = sorted(session_path.glob("*.IMA"))[0]
except IndexError as e:
    template_dcm = sorted(session_path.glob("*.dcm"))[0]
try:
    converter = Pdf2EncapsDCM()
    converted_dcm = converter.run(
        path_pdf=pdf_fn, path_template_dcm=template_dcm.as_posix(), suffix=".dcm"
    )[0]
    del report_output_dir, nifti_path

    print(f"Report created: {converted_dcm}")

    # Adding needed metadata to the report
    """"""
    pdf_dcm = dcmread(converted_dcm, stop_before_pixels=True)

    extra_metadata = [
        (
            "SeriesDescription",
            "0008,103e",
            "This is a rough brainmask",
        ),
    ]
    for info in extra_metadata:
        title = info[0]
        tag = info[1]
        description = info[2]
        # HACK this should be using the pydicom tag value but it's not working for some reason
        elem = pydicom.DataElement(title, "LO", description)
        pdf_dcm.DocumentTitle = "BrainyBarrier PDF Results"
        pdf_dcm.save_as(converted_dcm)

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
