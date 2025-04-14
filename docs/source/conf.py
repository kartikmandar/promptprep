import os
import sys

sys.path.insert(0, os.path.abspath("../.."))
# -- Project information -----------------------------------------------------

project = "promptprep"
copyright = "2025, Kartik Mandar"
author = "Kartik Mandar"

# -- General configuration ---------------------------------------------------

# Optional: Get version dynamically
try:
    import promptprep

    version = promptprep.__version__
    release = version
except ImportError:
    # Fallback if package can't be imported yet
    version = "0.1.10"
    release = version

extensions = [
    "sphinx.ext.autodoc",  # Core library for html generation from docstrings
    "sphinx.ext.napoleon",  # Support for NumPy and Google style docstrings
    "sphinx.ext.viewcode",  # Add links to highlighted source code
    "sphinx.ext.intersphinx",  # Link to other projects' documentation
    "sphinx.ext.autosectionlabel",  # Allow referencing sections with :ref:
    "sphinx.ext.todo",  # Support for todo items
    "sphinx.ext.coverage",  # Check documentation coverage
    "sphinx.ext.githubpages",  # Generate .nojekyll file for GitHub Pages
    "myst_parser",  # To parse Markdown files
]

# Autosectionlabel settings
autosectionlabel_prefix_document = True  # Prefix section labels with the document name

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = True
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}

# Theme settings
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "navigation_depth": 4,
    "titles_only": False,
    "logo_only": False,
    "display_version": True,
    "prev_next_buttons_location": "both",
    "style_external_links": True,
    "style_nav_header_background": "#2980B9",
}

# Other HTML settings
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_logo = None  # Add a logo file if you have one
html_favicon = None  # Add a favicon if you have one
html_show_sourcelink = True
html_show_sphinx = True
html_show_copyright = True

# Source parsing
source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

# Other settings
templates_path = ["_templates"]
exclude_patterns = []
todo_include_todos = True
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
]
