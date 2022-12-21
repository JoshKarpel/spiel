#!/usr/bin/env python

from datetime import datetime
from pathlib import Path

from textual.pilot import Pilot

from spiel.app import SpielApp

ROOT_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT_DIR / "docs" / "assets"
DECK_FILE = ROOT_DIR / "spiel" / "demo" / "demo.py"


async def auto_pilot(pilot: Pilot) -> None:
    app = pilot.app

    app.save_screenshot(filename="demo.svg", path=ASSETS_DIR)

    await pilot.press("d", "right", "down")

    app.save_screenshot(filename="deck.svg", path=ASSETS_DIR)

    await app.action_quit()


SpielApp(
    deck_path=DECK_FILE,
    watch_path=DECK_FILE.parent,
    show_messages=False,
    fixed_time=datetime(year=2022, month=12, day=17, hour=15, minute=31, second=42),
).run(
    headless=True,
    auto_pilot=auto_pilot,
    size=(130, 40),
)
