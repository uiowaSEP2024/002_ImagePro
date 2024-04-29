import logging

import pyorthanc
import requests


def check_study_has_properties(study: pyorthanc.Study) -> bool:
    for series in study.series:
        if (
            series.get_main_information()["MainDicomTags"]["SeriesDescription"]
            == "PROPERTIES"
        ):
            return True
    return False


class OrthancConnectionException(Exception):
    def __init__(self, msg: str = "Failed to connect to Orthanc") -> None:
        self.msg = msg
        super().__init__(self.msg)


class SingleStudyFailedException(Exception):
    def __init__(self, msg: str = "Study failed") -> None:
        self.msg = msg
        super().__init__(self.msg)


class SingleStudyFailedDownloadException(Exception):
    def __init__(self, msg: str = "Study failed to download") -> None:
        self.msg = msg
        super().__init__(self.msg)


def setup_custom_logger(name: str, log_level: int = logging.INFO):
    """
    Set up a custom logger with the specified name.
    """
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(module)s - %(message)s"
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.addHandler(handler)

    return logger


def format_time_delta_human_readable(time_delta: float) -> str:
    """
    Format a time delta in seconds to a human readable format.
    """
    minutes, seconds = divmod(time_delta, 60)
    return f" {int(minutes)}m {int(seconds)}s"


def ping_orthanc(orthanc_url: str) -> bool:
    """
    Ping the orthanc server to check if it is up.
    """
    try:
        requests.get(orthanc_url)
        return True
    except Exception:
        return False
