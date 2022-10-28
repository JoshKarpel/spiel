import sys
from importlib import metadata
from pathlib import Path

PACKAGE_NAME = "spiel"
__version__ = metadata.version(PACKAGE_NAME)
__rich_version__ = metadata.version("rich")
__textual_version__ = metadata.version("textual")
__python_version__ = ".".join(map(str, sys.version_info))

DECK = "deck"

PACKAGE_DIR = Path(__file__).resolve().parent
DEMO_DIR = PACKAGE_DIR / "demo"
DEMO_FILE = PACKAGE_DIR / "demo" / "demo.py"
