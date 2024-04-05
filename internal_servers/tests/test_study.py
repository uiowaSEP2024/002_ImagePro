import subprocess
import time
from unittest.mock import patch, MagicMock
from internal_servers.study import SingleStudyRun, StudyState
import pytest
from internal_servers.util_functions import ping_orthanc, OrthancConnectionException
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
    with patch("internal_servers.study.pyorthanc.Orthanc") as mock_orthanc:
        with patch(
            "internal_servers.study.SingleStudyRun._init_study_object"
        ) as mock_init_logger:
            with patch("internal_servers.study.pyorthanc.find") as mock_find:
                mock_study = MagicMock()
                mock_study.id_ = "1"
                mock_find.return_value = [mock_study]
                study_run = SingleStudyRun(
                    orthanc_url="http://localhost:8026",
                    study_id="1",
                    tracker_api_key="key",
                    study_config_file="config",
                    hospital_mapping_file="mapping",
                )

                assert study_run.study_status == StudyState.IN_PROGRESS
                assert study_run.study_id == "1"
                assert study_run.is_processed is False
                assert study_run.hospital_mapping == {"EXAMPLE_TOOL": "EXAMPLE_TOOL"}
                mock_orthanc.assert_called_once_with("http://localhost:8026")
                mock_init_logger.assert_called_once()


def test_study_status_methods():
    with patch("internal_servers.study.pyorthanc.find") as mock_find:
        mock_study = MagicMock()
        mock_study.id_ = "1"
        mock_find.return_value = [mock_study]
        study_run = SingleStudyRun(
            orthanc_url=internal_orthanc_url,
            study_id="1",
            tracker_api_key="key",
            study_config_file="config",
            hospital_mapping_file="mapping",
        )
        assert study_run.get_study_is_in_progress() is True
        assert study_run.get_study_is_completed() is False
        assert study_run.get_study_is_errored() is False
        assert study_run.get_study_is_failed() is False


def test_init_orthanc_connection_success():
    with patch("internal_servers.study.pyorthanc.Orthanc") as mock_orthanc:
        _ = SingleStudyRun(
            orthanc_url=internal_orthanc_url,
            study_id="1",
            tracker_api_key="key",
            study_config_file="config",
            hospital_mapping_file="mapping",
        )
        mock_orthanc.assert_called_once_with("http://localhost:8026")


def test_init_orthanc_connection_failure():
    with patch(
        "internal_servers.study.pyorthanc.Orthanc", side_effect=Exception("Error")
    ):
        with pytest.raises(OrthancConnectionException):
            _ = SingleStudyRun(
                orthanc_url="http://localhost:9999",
                study_id="1",
                tracker_api_key="key",
                study_config_file="config",
                hospital_mapping_file="mapping",
            )


def test_get_hospital_return_aet_mapping():
    study_run = SingleStudyRun(
        orthanc_url=internal_orthanc_url,
        study_id="1",
        tracker_api_key="key",
        study_config_file="config",
        hospital_mapping_file="mapping",
    )
    # This test is kinda useless and needs to be refactored once the actual implementation is done
    mapping = study_run._get_hospital_return_aet_mapping("mapping")
    assert mapping == {"EXAMPLE_TOOL": "EXAMPLE_TOOL"}


def test_study_is_stable():
    with patch("internal_servers.study.pyorthanc.Study") as mock_study:
        mock_study.get_main_information.return_value = {"IsStable": True}
        study_run = SingleStudyRun(
            orthanc_url=internal_orthanc_url,
            study_id="1",
            tracker_api_key="key",
            study_config_file="config",
            hospital_mapping_file="mapping",
        )
        assert study_run.study_is_stable() is True


def test_study_has_properties():
    # Create a mock series object with the desired return value for the get_main_information method.
    mock_series = MagicMock()
    mock_series.get_main_information.return_value = {
        "MainDicomTags": {"SeriesDescription": "PROPERTIES"}
    }

    # Mock the Study object's series attribute to be a list containing our mock series.
    with patch("internal_servers.study.pyorthanc.Study") as mock_study:
        mock_study.series = [mock_series]

        # Initialize the SingleStudyRun object with the required parameters.
        study_run = SingleStudyRun(
            orthanc_url="internal_orthanc_url",
            study_id="1",
            tracker_api_key="key",
            study_config_file="config",
            hospital_mapping_file="mapping",
        )

        # Set the study attribute of the SingleStudyRun instance to the mock_study
        study_run.study = mock_study

        # The actual test: checking if the study_run.study_has_properties() returns True.
        assert study_run.study_has_properties() is True


def test_init_study_logger():
    with patch("internal_servers.study.OrthancStudyLogger") as mock_logger:
        study_run = SingleStudyRun(
            orthanc_url=internal_orthanc_url,
            study_id="1",
            tracker_api_key="key",
            study_config_file="config",
            hospital_mapping_file="mapping",
        )
        study_run._init_study_logger()
        mock_logger.assert_called_once_with(
            hospital_id="EXAMPLE_TOOL",
            study_id="1",
            tracker_api_key="key",
            study_config_file="config",
        )


def test_init_study_object():
    with patch("internal_servers.study.pyorthanc.find") as mock_find:
        mock_study = MagicMock()
        mock_study.id_ = "1"
        mock_find.return_value = [mock_study]
        study_run = SingleStudyRun(
            orthanc_url=internal_orthanc_url,
            study_id="1",
            tracker_api_key="key",
            study_config_file="config",
            hospital_mapping_file="mapping",
        )
        assert study_run.study.id_ == "1"


def test_init_study_object_study_doesnt_exist():
    with patch("internal_servers.study.pyorthanc.find") as mock_find:
        mock_find.return_value = []
        study_run = SingleStudyRun(
            orthanc_url=internal_orthanc_url,
            study_id="1",
            tracker_api_key="key",
            study_config_file="config",
            hospital_mapping_file="mapping",
        )
        assert study_run.study_status == StudyState.ERROR


def test_study_can_download():
    pass


def test_study_can_call_example_tool():
    pass


def test_study_can_upload():
    pass


def test_study_can_log():
    pass


def test_study_can_return_completed():
    pass
