#!/usr/bin/env python

from collections.abc import Iterable
from datetime import datetime
from functools import partial
from io import StringIO
from pathlib import Path

from more_itertools import intersperse
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


async def auto_pilot(pilot: Pilot, name: str, keys: Iterable[str]) -> None:
    await pilot.press(*intersperse("wait:100", keys))

    (ASSETS_DIR / name).with_suffix(".svg").write_text(take_reproducible_screenshot(pilot.app))

    await pilot.app.action_quit()


def take_screenshot(name: str, size: tuple[int, int], keys: Iterable[str]) -> None:
    SpielApp(
        deck_path=DECK_FILE,
        watch_path=DECK_FILE.parent,
        show_messages=False,
        fixed_time=datetime(year=2022, month=12, day=17, hour=15, minute=31, second=42),
    ).run(
        headless=True,
        auto_pilot=partial(auto_pilot, name=name, keys=keys),
        size=size,
    )


take_screenshot(name="demo", size=(130, 35), keys=())
take_screenshot(name="deck", size=(130, 35), keys=("d", "right", "down"))
take_screenshot(name="help", size=(110, 35), keys=("?",))
