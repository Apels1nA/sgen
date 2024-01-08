# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'SGen'
copyright = '2024, Ilya Verner'
author = 'Ilya Verner'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'alabaster',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme_options = {
    "logo": "sgen-logo.png",
    "logo_name": "",
    "logo_only": False,
    "description": "Generating test data structures",
    "description_font_style": "italic",
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
