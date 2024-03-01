FROM ubuntu:latest
LABEL authors="iejohnson"

# Use Ubuntu as base image
FROM ubuntu:latest

# Set environment variables
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PATH /opt/venv/bin:$PATH

# Install necessary libraries
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3.10-venv \
    git \
    curl \
    libsm6 \
    libxext6 \
    libxrender-dev

# Upgrade pip
RUN python3.10 -m pip install --upgrade pip

# Create a virtual environment and activate it
RUN python3.10 -m pip install --user virtualenv
RUN python3.10 -m venv /opt/venv
RUN . /opt/venv/bin/activate

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY ../requirements_medical_tool.txt .

# Install Python dependencies
RUN pip install -r requirements_medical_tool.txt

# Copy the rest of the code
COPY brainmask_tool.py /app/brainmask_tool.py
COPY cnn_transforms.py /app/cnn_transforms.py
COPY pdf_report.py /app/pdf_report.py
COPY rf_dicom_modality_classifier.onnx /app/rf_dicom_modality_classifier.onnx
COPY brainmask_model.ckpt /app/brainmask_model.ckpt

# TODO Check the code below. Im not sure if this is what we actually want
# The desired functionality is to have a mounted directory for input and output files
# I want to be able to run the container with the input and output directories as arguments
# Then I want to be able to trigger the tool to run with an extra parameter that is the study_id
# The tool should then read the input files, process them and write the output files to the output directory
# Add an environment variable for the input directory
ENV INPUT_DIR /input
# Add an environment variable for the output directory
ENV OUTPUT_DIR /output

ARG STUDY_ID=""

ENTRYPOINT = ["python", "brainmask_tool.py", "--input_dir", "$INPUT_DIR", "--output_dir", "$OUTPUT_DIR", "--study_id", "$STUDY_ID"]
