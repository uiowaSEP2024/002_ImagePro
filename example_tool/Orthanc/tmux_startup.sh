#!/bin/bash
# If you don't have tmux installed check the following link:
# https://github.com/tmux/tmux/wiki/Installing
orthanc_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Prompt the user if they want to kill all Orthanc processes
echo "Do you want to kill all Orthanc processes before starting? (y/n)"
read kill_answer
if [ "$kill_answer" = "y" ]; then
    echo "Killing all Orthanc processes..."
    killall Orthanc || echo "No Orthanc processes were found running."
fi

# Start TMUX session
tmux new-session -d -s example_tool_testing

# Create windows for running hospital and internal PACS
tmux new-window -d -t example_tool_testing -n run_hospital
tmux send-keys -t example_tool_testing:run_hospital.0 '/bin/bash $(pwd)/run_hospital.sh' C-m

tmux new-window -d -t example_tool_testing -n run_internal_pacs
tmux send-keys -t example_tool_testing:run_internal_pacs.0 '/bin/bash $(pwd)/run_internal_pacs.sh' C-m

# Prompt for uploading example data
echo "Do you want to upload example data? (y/n)"
read upload_answer
if [ "$upload_answer" = "y" ]; then
  # Create a new window for uploading data
  tmux new-window -d -t example_tool_testing -n upload_data
  tmux send-keys -t example_tool_testing:upload_data.0 "python3 '${orthanc_dir}/upload_example_data_to_hospital.py'" C-m
fi

# Attach to the session
tmux attach -t example_tool_testing
