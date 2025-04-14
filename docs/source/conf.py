import os
import sys

sys.path.insert(0, os.path.abspath('../..'))
# -- Project information -----------------------------------------------------

project = 'promptprep'
copyright = '2025, Kartik Mandar'
author = 'Kartik Mandar'
release = '0.1.10'

# -- General configuration ---------------------------------------------------

# Optional: Get version dynamically
try:
    import promptprep
    version = promptprep.__version__
    release = version
except ImportError:
     # Fallback if package can't be imported yet
    version = '0.1.10'
    release = version

extensions = [
    'sphinx.ext.autodoc',      # Core library for html generation from docstrings
    'sphinx.ext.napoleon',     # Support for NumPy and Google style docstrings
    'sphinx.ext.viewcode',     # Add links to highlighted source code
    'sphinx.ext.intersphinx',  # Link to other projects' documentation (optional but good)
    'myst_parser',             # To parse Markdown files
]

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

html_theme = "sphinx_rtd_theme"



templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']


source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}