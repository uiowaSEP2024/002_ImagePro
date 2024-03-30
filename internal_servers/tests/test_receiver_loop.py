import pytest
from unittest.mock import patch, MagicMock
from internal_servers.receiver_loop import ReceiverLoop


@pytest.fixture
def receiver():
    with patch("pyorthanc.Orthanc", return_value=MagicMock()):
        return ReceiverLoop(
            "http://localhost", "api_key", "hospital_mapping", "study_config"
        )


def test_check_for_new_studies_new_study_found(receiver):
    mock_series = MagicMock()
    mock_series.get_main_information.return_value = {
        "MainDicomTags": {"SeriesDescription": "PROPERTIES"}
    }
    # Ensure the MagicMock simulates the study object as expected
    mock_study = MagicMock(id_="new_study", series=[mock_series])

    with patch("pyorthanc.find_studies", return_value=[mock_study]), patch(
        "internal_servers.util_functions.check_study_has_properties", return_value=True
    ):
        receiver._check_for_new_studies()
        assert (
            "new_study" in receiver.studies_dict
        ), "New study should be added to studies_dict"


def test_check_for_new_studies_no_new_study_found(receiver):
    with patch("pyorthanc.find_studies", return_value=[]):
        receiver._check_for_new_studies()
        assert len(receiver.studies_dict) == 0


def test_check_for_completed_studies_with_completed_study(receiver):
    mock_study_run = MagicMock()
    mock_study_run.get_study_is_in_progress.return_value = False
    receiver.studies_dict = {"completed_study": mock_study_run}
    receiver.check_for_completed_studies()
    assert "completed_study" not in receiver.studies_dict


def test_check_for_completed_studies_with_in_progress_study(receiver):
    mock_study_run = MagicMock()
    mock_study_run.get_study_is_in_progress.return_value = True
    receiver.studies_dict = {"in_progress_study": mock_study_run}
    receiver.check_for_completed_studies()
    assert "in_progress_study" in receiver.studies_dict


def test_check_for_new_studies_study_missing_properties(receiver):
    mock_study = MagicMock(id_="invalid_study")
    with patch("pyorthanc.find_studies", return_value=[mock_study]), patch(
        "internal_servers.util_functions.check_study_has_properties", return_value=False
    ):
        with pytest.raises(ValueError) as exc_info:
            receiver._check_for_new_studies()
        assert "does not have the required properties" in str(exc_info.value)
