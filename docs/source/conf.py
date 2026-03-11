# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'TRAFIKK Pipeline'
copyright = '2026, Marco Fariñas and Viviam Bermúdez'
author = 'Marco Fariñas and Viviam Bermúdez'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx.ext.mathjax",
]

myst_enable_extensions = [
    "dollarmath",
]

templates_path = ['_templates']
exclude_patterns = []

suppress_warnings = ["config.cache"]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_material'
html_static_path = ['_static']
html_theme_options = {
    'nav_title': 'TRAFIKK Pipeline Documentation',
    'theme_color': 'deep_purple',
    'color_primary': 'deep_purple',
    'color_accent': 'red',
    'logo_icon': '&#xe865',
    'globaltoc_depth': 3,         
    'globaltoc_includehidden': True,
}

html_sidebars = {
    "**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"],
}

html_title = "User Guide"