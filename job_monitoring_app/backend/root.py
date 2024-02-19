"""
This file must be kept in the root of the backend
"""
import os
from pathlib import Path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def root_path(path=""):
    return Path(ROOT_DIR) / path
