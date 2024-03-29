import subprocess
import time

import pytest
from internal_servers.util_functions import ping_orthanc
from pathlib import Path

internal_orthanc_url = "http://localhost:8026"
hospital_orthanc_url = "http://localhost:8030"


def kill_all_orthanc_processes():
    """
    Hard stop the orthanc server
    """
    subprocess.run(["pkill", "-f", "Orthanc"])


@pytest.fixture(scope="session", autouse=True)
def orthanc_server(tmp_path_factory):
    current_dir = Path(__file__).parent
    relative_orthanc_paths = current_dir.parent.parent / "example_tool" / "Orthanc"
    internal_orthanc_startup_path = relative_orthanc_paths / "run_internal_pacs.sh"
    hospital_orthanc_startup_path = relative_orthanc_paths / "run_hospital.sh"
    # Adjust this path
    if not internal_orthanc_startup_path.exists():
        raise FileNotFoundError(
            f"Internal Orthanc startup script not found at {internal_orthanc_startup_path}"
        )

    # Start internal Orthanc
    internal_orthanc_log = tmp_path_factory.mktemp("logs") / "internal_orthanc.log"
    _ = subprocess.Popen(
        ["bash", str(internal_orthanc_startup_path)],
        stdout=internal_orthanc_log.open("w"),
        start_new_session=True,
        stderr=subprocess.STDOUT,
    )
    hospital_orthanc_log = tmp_path_factory.mktemp("logs") / "hospital_orthanc.log"
    _ = subprocess.Popen(
        ["bash", hospital_orthanc_startup_path.as_posix()],
        stdout=hospital_orthanc_log.open("w"),
        start_new_session=True,
        stderr=subprocess.STDOUT,
    )

    print(
        f"Started Orthanc servers at {internal_orthanc_url}  sleeping 15 seconds to ensure they are up"
    )
    # Wait for Orthanc servers to be up
    time.sleep(15)  # Adjust this based on how long Orthanc takes to start
    yield internal_orthanc_url, hospital_orthanc_url

    kill_all_orthanc_processes()


def test_orthanc_server_is_up():
    assert (
        ping_orthanc(internal_orthanc_url) is True
    ), "Orthanc server doesnt seem to be up, please run the setup_orthancs_for_testing_suite.py"
    assert (
        ping_orthanc(hospital_orthanc_url) is True
    ), "Orthanc server doesnt seem to be up, please run the setup_orthancs_for_testing_suite.py"


def test_single_study_run_initialization():
    pass
    # study = SingleStudyRun(
    #     orthanc_url=internal_orthanc_url,
    #     study_id=""


# def test_ensure_orthanc_is_up():
#     """
#     Test that the orthanc server is up
#     """
#     # Add more assertions based on what you expect to be initialized.
#     study = SingleStudyRun(
#         orthanc_url=internal_orthanc_url,
#         study_id=

# def test_single_study_run_initialization(mocker):
#
#     # Add more assertions based on what you expect to be initialized.
