#!/usr/bin/env python3
import sys
import argparse

import pydicom
from pdf2dcm import Pdf2EncapsDCM, Pdf2RgbSC
from subprocess import run
from pipeline_functions import *
from pdf_report import generate_report
from pydicom import dcmread
from pathlib import Path
from enum import Enum, auto



description = "author: Michal Brzus\nBrainmask Tool\n"

# parse command line
parser = argparse.ArgumentParser(description=description)
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


stage_name = "input_validation_and_conversion"
print(f"Running stage: {stage_name}")
# create output directory
if not Path(args.output_dir).exists():
    print("Creating output directory")
    run(["mkdir", "-p", args.output_dir])

# run dicom inference and NIfTI conversion
print("Processing DICOM data")
session_path = Path(args.session_dir)
output_path = Path(args.output_dir)


try :
    nifti_path = dicom_inference_and_conversion(
        session_dir=session_path.as_posix(),
        output_dir=output_path.as_posix(),
        model_path="./rf_dicom_modality_classifier.onnx",
    )
except Exception as e:
    print(f"Error in stage: {stage_name}")
    print(e)
    sys.exit(1)

print("NIfTI files created")
print(f"Successfully finished stage: {stage_name}")

stage_name = "brainmask_inference"
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
    brainmask_inference(data_dict, "brainmask_model.ckpt", brainmask_output_dir)
except Exception as e:
    print(f"Error in stage: {stage_name}")
    print(e)
    sys.exit(1)
# create output directory for report
report_output_dir = Path(nifti_path).parent.as_posix() + "/report"
if not Path(report_output_dir).exists():
    print("Creating report output directory")
    run(["mkdir", "-p", report_output_dir])


# generate report

print(f"Running stage: {stage_name}")
im_path = raw_anat_nifti_files[0]
mask_path = list(Path(brainmask_output_dir).glob("*.nii.gz"))[0]
stage_name = "report_generation"
try:
    pdf_fn = generate_report(im_path.as_posix(), mask_path.as_posix(), report_output_dir)
    print(f"Report created: {pdf_fn}")
except Exception as e:
    print(f"Error in stage: {stage_name}")
    print(e)
    sys.exit(1)

stage_name = "pdf_to_dcm_conversion"
# This assumes that the template IMA file is in the session directory and that the first IAM file is the valid
template_dcm = sorted(session_path.glob("*.IMA"))[0]

try:
    converter = Pdf2EncapsDCM()
    converted_dcm = converter.run(path_pdf=pdf_fn, path_template_dcm=template_dcm.as_posix(), suffix =".dcm")[0]
    del report_output_dir, brainmask_output_dir, nifti_path

    print(f"Report created: {converted_dcm}")

    # Adding needed metadata to the report
    """"""
    pdf_dcm = dcmread(converted_dcm,stop_before_pixels=True)


    extra_metadata = [
    (
        "SeriesDescription",
        "0008,103e",
        f"This is a rough brainmask",
    ),
    ]
    for info in extra_metadata:
        title = info[0]
        tag = info[1]
        description = info[2]
        # HACK this should be using the pydicom tag value but it's not working for some reason
        elem = pydicom.DataElement(title, "LO", description)
        pdf_dcm.DocumentTitle = f"BrainyBarrier PDF Results: for {im_path.stem}"
        pdf_dcm.save_as(converted_dcm)

except Exception as e:
    print(f"Error in stage: {stage_name}")
    print(e)
    sys.exit(1)

print(f"Successfully finished stage: {stage_name}")


# [ 'tests/test_data/test_file.dcm' ]