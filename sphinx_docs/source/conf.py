# Paths to the backend and trackerapi directories are added to the system path
import os
import sys

# Determine the absolute path to the directory containing conf.py
docs_dir = os.path.dirname(os.path.abspath(__file__))
# Calculate the path to the root of the project, assuming conf.py is two levels down from the project root
project_root = os.path.dirname(os.path.dirname(docs_dir))

# Add directories to sys path
sys.path.insert(0, project_root)  # Add the project root to the system path
sys.path.insert(
    0, os.path.join(project_root, "job_monitoring_app/backend")
)  # Add the backend directory to the system path
sys.path.insert(
    0, os.path.join(project_root, "job_monitoring_app/trackerapi")
)  # Add the trackerapi directory to the system path
sys.path.insert(
    0, os.path.join(project_root, "internal_servers")
)  # Add the internal_servers directory to the system path
sys.path.insert(
    0, os.path.join(project_root, "example_tool_light")
)  # Add the example_tool_light directory to the system path
sys.path.insert(
    0, os.path.join(project_root, "example_tool")
)  # Add the example_tool directory to the system path
sys.path.insert(
    0, os.path.join(project_root, "sphinx_docs")
)  # Add the sphinx_docs directory to the system path


# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "job_monitoring_app"
copyright = "2024, Zach Morris, Ivan Johnson, Audrey Powers, Michal Brzus"
author = "Zach Morris, Ivan Johnson, Audrey Powers, Michal Brzus"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc"]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]
