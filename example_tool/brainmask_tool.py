#!/usr/bin/env python3
import sys
import argparse

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


from subprocess import run
from pipeline_functions import *
from pathlib import Path

# create output directory
if not Path(args.output_dir).exists():
    print("Creating output directory")
    run(["mkdir", "-p", args.output_dir])

# run dicom inference and NIfTI conversion
print("Processing DICOM data")
nifti_path = dicom_inference_and_conversion(
    session_dir=args.session_dir,
    output_dir=args.output_dir,
    model_path="./rf_dicom_modality_classifier.onnx",
)
print("NIfTI files created")

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
print("Running brainmask inference")
brainmask_inference(data_dict, "brainmask_model.ckpt", brainmask_output_dir)


