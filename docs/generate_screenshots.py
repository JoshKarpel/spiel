#!/usr/bin/env python

from datetime import datetime
from io import StringIO
from pathlib import Path

from rich.console import Console
from textual.app import App
from textual.pilot import Pilot

from spiel.app import SpielApp

ROOT_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT_DIR / "docs" / "assets"
DECK_FILE = ROOT_DIR / "spiel" / "demo" / "demo.py"


def take_reproducible_screenshot(app: App[object]) -> str:
    """
    Textual's screenshot functions don't let you control the unique_id argument to console.export_svg,
    so this little shim just reproduces the internals of Textual's methods with more control.
    """
    width, height = app.size
    console = Console(
        width=width,
        height=height,
        file=StringIO(),
        force_terminal=True,
        color_system="truecolor",
        record=True,
        legacy_windows=False,
    )
    screen_render = app.screen._compositor.render(full=True)
    console.print(screen_render)
    return console.export_svg(title=app.title, unique_id="spieldocs")


async def auto_pilot(pilot: Pilot) -> None:
    app = pilot.app

    (ASSETS_DIR / "demo.svg").write_text(take_reproducible_screenshot(app))

    await pilot.press("d", "right", "down")

    (ASSETS_DIR / "deck.svg").write_text(take_reproducible_screenshot(app))

    await app.action_quit()


SpielApp(
    deck_path=DECK_FILE,
    watch_path=DECK_FILE.parent,
    show_messages=False,
    fixed_time=datetime(year=2022, month=12, day=17, hour=15, minute=31, second=42),
).run(
    headless=True,
    auto_pilot=auto_pilot,
    size=(130, 35),
)
