from importlib import metadata

PACKAGE_NAME = "spiel"
__version__ = metadata.version(PACKAGE_NAME)
__rich_version__ = metadata.version("rich")

DECK = "DECK"
