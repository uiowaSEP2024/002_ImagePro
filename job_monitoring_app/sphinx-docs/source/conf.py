# Paths to the backend and trackerapi directories are added to the system path
import os
import sys

# sys.path.insert(0, os.path.abspath("../../backend"))
# sys.path.insert(0, os.path.abspath("../../trackerapi"))

# Determine the absolute path to the directory containing conf.py
docs_dir = os.path.dirname(os.path.abspath(__file__))
# Calculate the path to the root of the project, assuming conf.py is two levels down from the project root
project_root = os.path.dirname(os.path.dirname(docs_dir))

# Add the 'backend' and 'trackerapi' directories to sys.path
sys.path.insert(0, os.path.join(project_root, "backend"))
sys.path.insert(0, os.path.join(project_root, "trackerapi"))


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
