# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "GeoNode Cloud Core"
copyright = "2024, Kan Territory & IT"
author = "Kan Territory & IT"
release = "1.0.0"

import sys

sys.setrecursionlimit(1500)

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx.ext.todo",
    "sphinx.ext.autosummary",
    "sphinxcontrib.openapi",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "autoapi.extension",  # Genera documentación a partir de los docstrings.
]

templates_path = ["_templates"]
exclude_patterns = []

autoapi_dirs = ["../../geonode-cloud-core"]
autoapi_ignore = [
    "**/docs/**",
    "**/.circleci/**",
    "**/.devcontainer/**",
    "**/.github/**",
    "**/.tx/**",
    "**/migrations/**",
]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

language = "en"
locale_dirs = ["locale/"]  # Directorio que contiene los archivos de traducción
gettext_compact = False  # Para evitar la compresión de mensajes en un solo archivo
