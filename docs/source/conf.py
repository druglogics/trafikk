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
    "colon_fence",
    "html_image",
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
html_css_files = ['custom.css']

html_theme_options = {
    'nav_title': 'TRAFIKK',
    'theme_color': '#6c3ec1',
    'color_primary': 'deep-purple',
    'color_accent': 'pink',
    'logo_icon': '&#xe865',
    'globaltoc_depth': 3,
    'globaltoc_includehidden': True,
    'globaltoc_collapse': True,
    'heroes': {
        'index': 'Systematic prediction and mechanistic interpretation of anticancer drug synergies',
    },
    'repo_url': 'https://github.com/druglogics/trafikk',
    'repo_name': 'trafikk',
    'repo_type': 'github',
    'master_doc': True,
    'nav_links': [],
}

html_sidebars = {
    "**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"],
}

html_title = "TRAFIKK Docs"