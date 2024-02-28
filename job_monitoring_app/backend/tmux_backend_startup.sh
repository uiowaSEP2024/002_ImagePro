#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )  # Get the directory of the script

# Check if the user has provided an argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <path_to_venv>"
    exit 1
fi

VENV_PATH=$1 # Store the first argument as the path to the virtual environment

# Check if virtual environment exists at the given path
if [ ! -d "$VENV_PATH" ]; then
    # Create a virtual environment at the specified path
    run "python3 -m venv $VENV_PATH"
    # Activate the virtual environment
    source "$VENV_PATH"/bin/activate
    # Install the required packages
    pip install -r requirements.txt
else
    # Activate the virtual environment
    source "$VENV_PATH"/bin/activate
    # Update the required packages to the latest version
    pip install -r requirements.txt
fi

export APP_ENV='development' # Set the environment variable to development #TODO make this an argument
# Create a new tmux session and window
tmux new-session -d -s backend_session


tmux new-window -d -t backend_session -n run_database
# Start the virtual environment in the first pane
tmux send-keys -t backend_session:run_database.0 "source $VENV_PATH/bin/activate" C-m
tmux send-keys -t backend_session:run_database.0 "cd $SCRIPT_DIR" C-m
tmux send-keys -t backend_session:run_database.0 "/bin/bash run-db.sh" C-m


tmux new-window -d -t backend_session -n run_backend
# Also start the virtual environment in the second pane
tmux send-keys -t backend_session:run_backend.0 "source $VENV_PATH/bin/activate" C-m
tmux send-keys -t backend_session:run_backend.0 "cd $SCRIPT_DIR" C-m
#tmux send-keys -t backend_session:run_database.0 "/bin/bash alembic upgrade head" C-m # TODO: add this line in the future
tmux send-keys -t backend_session:run_backend.0 "/bin/bash run-dev.sh" C-m

# Attach to the tmux session
tmux attach-session -t backend_session
