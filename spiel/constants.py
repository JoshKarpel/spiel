from __future__ import annotations

import sys
from enum import Enum
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

FOOTER_TIME_FORMAT = "%Y-%m-%d %I:%M %p"
RELOAD_MESSAGE_TIME_FORMAT = "%I:%M:%S %p"


class Direction(Enum):
    Right = "right"
    Left = "left"


class TransitionEffect(Enum):
    Instant = "instant"
    Swipe = "swipe"
