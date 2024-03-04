#!/bin/bash
CURRENT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )  # Get the directory of the script
# Default values
DEFAULT_INPUT_DIR="${CURRENT_DIR}/example_tool/example_data/CAIPIRINHA_SPACE_Neuro_Head_Examples"
DEFAULT_OUTPUT_DIR="${CURRENT_DIR}/example_tool/example_output"
DEFAULT_STUDY_ID="12345"

# Use provided arguments if they exist, otherwise use default values
INPUT_DIR=${1:-$DEFAULT_INPUT_DIR}
OUTPUT_DIR=${2:-$DEFAULT_OUTPUT_DIR}
STUDY_ID=${3:-$DEFAULT_STUDY_ID}

if [ ! -d "$INPUT_DIR" ]; then
  echo "Input directory does not exist: $INPUT_DIR"
  exit 1
fi
if [ ! -d "$OUTPUT_DIR" ]; then
  echo "Output directory does not exist: $OUTPUT_DIR"
  echo "Creating output directory: $OUTPUT_DIR"
  mkdir -p "$OUTPUT_DIR"
fi


docker run --rm \
-v $INPUT_DIR:/input \
-v $OUTPUT_DIR:/output \
brainmasktool:v0.1\
 -s /input \
 -o /output\
 -i "$DEFAULT_STUDY_ID"
