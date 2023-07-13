#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import os
import sys
import typing

import pyairtable.api.types
import pyairtable.orm.fields
from pyairtable import __version__ as version

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "sphinxext.opengraph",
    "sphinx.ext.autosectionlabel",
    # "autoapi.extension",
    "sphinx_autodoc_typehints",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# Open Graph extension config. https://pypi.org/project/sphinxext-opengraph/
ogp_site_url = "https://pyairtable.readthedocs.io/"
ogp_image = "https://pyairtable.readthedocs.io/en/master/_images/logo.png"
ogp_description_length = 300

ogp_custom_meta_tags = [
    '<meta name="twitter:card" content="summary_large_image">',
]

# See https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
autodoc_class_signature = "separated"
autodoc_default_options = {
    "exclude-members": "__new__",
}
autodoc_member_order = "bysource"

# See https://github.com/tox-dev/sphinx-autodoc-typehints#options
typehints_defaults = "comma"
typehints_use_signature = True
typehints_use_signature_return = True


def typehints_formatter(annotation, config):
    """
    Provide links from function signatures to TypedDict docstrings.
    """
    for name, value in vars(pyairtable.api.types).items():
        if annotation != value:
            continue
        if isinstance(value, type) and issubclass(value, dict):  # TypedDict
            return f":data:`~pyairtable.api.types.{name}`"
        if isinstance(value, typing._GenericAlias):  # Union, Dict, etc.
            return f":data:`~pyairtable.api.types.{name}`"

    if annotation == typing.Literal[pyairtable.orm.fields._LinkFieldOptions.LinkSelf]:
        return ":data:`~pyairtable.orm.fields.LinkSelf`"
    if annotation == pyairtable.orm.fields.T_Linked:
        return ":class:`~pyairtable.orm.Model`"

    return None


# Needed for autoapi to not choke on retrying.Retry
suppress_warnings = ["autoapi.python_import_resolution"]


################################
# CUSTOM
################################

source_dir = os.path.dirname(__file__)
doc_dir = os.path.dirname(source_dir)
root_dir = os.path.dirname(doc_dir)
sys.path.append(root_dir)

# Document Python Code
autoapi_type = "python"
autoapi_dirs = [os.path.join(root_dir, "pyairtable")]
# add_module_names = False

napoleon_google_docstring = True
napoleon_include_init_with_doc = True
napoleon_attr_annotations = True
# napoleon_preprocess_types = True  # True to convert the type definitions in the docstrings as references. Defaults to False.
# napoleon_type_aliases = None
# napoleon_attr_annotations = True
# napoleon_use_param = True

__version__ = version.split("-", 0)
__release__ = version

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
# version = '0.2.0.dev1'
# The full version, including alpha/beta/rc tags.
# release = '0.2.0.dev1'

html_theme = "revitron_sphinx_theme"

################################
# CUSTOM
################################

source_suffix = ".rst"
master_doc = "index"

# General information about the project.
project = "pyAirtable"
copyright = "2021, Gui Talarico"
author = "Gui Talarico"


# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
# pygments_style = "sphinx"
pygments_style = "monokai"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}
html_theme_options = {
    # "color_scheme": "",
    # "canonical_url": "",
    "analytics_id": "UA-3836052-10",
    # "style_external_links": False,
    # "collapse_navigation": True,
    # "sticky_navigation": True,
    # "navigation_depth": 4,
    # "includehidden": True,
    # "titles_only": False,
    "github_url": "https://github.com/gtalarico/pyairtable",
    # 'logo_mobile': 'demo/static/logo-mobile.svg'
    # "logo_mobile": "_static/logo.png",
}

# html_logo = 'demo/static/logo.svg'
html_logo = "_static/logo-text.svg"

html_context = {
    "landing_page": {
        "menu": [
            # {"title": "Airtable Api Docs", "url": "https://airtable.com/api"},
            # {"title": "♡ Sponsor", "url": "https://github.com/sponsors/gtalarico"},
        ]
    },
    "docs_source_path": "main/docs/source",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']
html_css_files = ["custom.css"]
# html_js_files = []
