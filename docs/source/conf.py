# Configuration file for the Sphinx documentation builder.

# -- Project information

project = "django-single-session"
copyright = "2022, Willem Van Onsem"
author = "Willem Van Onsem"

release = "0.1"
version = "0.1.0"

from os import environ
from os.path import dirname
from sys import path

path.insert(0, dirname(dirname(dirname(__file__))))
environ.setdefault("DJANGO_SETTINGS_MODULE", "docs.source.settings")

import django

django.setup()

# -- General configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output

# html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = "footnote"
