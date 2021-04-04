import sys
from importlib import metadata

PACKAGE_NAME = "spiel"
__version__ = metadata.version(PACKAGE_NAME)
__rich_version__ = metadata.version("rich")
__python_version__ = ".".join(map(str, sys.version_info))

DECK = "DECK"

TARGET_RPS = 30
