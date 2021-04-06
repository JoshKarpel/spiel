import sphinx_rtd_theme

import spiel

project = spiel.constants.PACKAGE_NAME.capitalize()
copyright = "2021, Josh Karpel"
author = "Josh Karpel"
release = spiel.constants.__version__


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_rtd_theme",
]

templates_path = ["_templates"]
html_static_path = ["_static"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"

# sphinx-autodoc
autoclass_content = "both"
autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
}
autodoc_typehints = "signature"

# sphinx-autodoc-typehints
set_type_checking_flag = True
