from unittest.mock import Mock
from internal_servers.orthanc_reciever_agent import (
    check_study_stable,
)  # Ensure you import your function correctly


def test_check_study_stable():
    study_mock = Mock()
    study_mock.get_main_information.return_value = {"IsStable": True}
    assert check_study_stable(study_mock) is True

    study_mock.get_main_information.return_value = {"IsStable": False}
    assert check_study_stable(study_mock) is False

    study_mock.get_main_information.side_effect = Exception("Error")
    assert check_study_stable(study_mock) is False
