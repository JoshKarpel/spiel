import sys
from importlib import metadata

PACKAGE_NAME = "spiel"
__version__ = metadata.version(PACKAGE_NAME)
__rich_version__ = metadata.version("rich")
__textual_version__ = metadata.version("textual")
__python_version__ = ".".join(map(str, sys.version_info))

DECK = "deck"
