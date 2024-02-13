#!/bin/bash
# If you don't have tmux installed check the following link:
# https://github.com/tmux/tmux/wiki/Installing

# Prompt the user if they want to kill all Orthanc processes
echo "Do you want to kill all Orthanc processes before starting? (y/n)"
read answer
if [ "$answer" = "y" ]; then
    echo "Killing all Orthanc processes..."
    killall Orthanc || echo "No Orthanc processes were found running."
fi

# Proceed with your TMUX session setup
tmux new-session -d -s example_tool_testing

tmux new-window -d -t example_tool_testing -n run_hospital
tmux send-keys -t example_tool_testing:run_hospital.0 '/bin/bash $(pwd)/run_hospital.sh' C-m

tmux new-window -d -t example_tool_testing -n run_internal_pacs
tmux send-keys -t example_tool_testing:run_internal_pacs.0 '/bin/bash $(pwd)/run_internal_pacs.sh' C-m

# Attach to the session
tmux a -t example_tool_testing
