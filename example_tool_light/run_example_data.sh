#!/bin/bash
# from https://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )  # Get the directory of the script
brains_tool_path="${SCRIPT_DIR}/brainmask_tool.py"  # Get the path to the brains_tool.py
example_data_path="${SCRIPT_DIR}/example_data/CAIPIRINHA_SPACE_Neuro_Head_Examples"  # Get the path to the example_data
example_output_path="${SCRIPT_DIR}/example_output"  # Get the path to the example_output
python3 "${brains_tool_path}" \
-i "skjsdkhsd" \
-s "${example_data_path}" \
-o "${example_output_path}"\
