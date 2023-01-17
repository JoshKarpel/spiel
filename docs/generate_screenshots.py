#!/usr/bin/env python

import os
from collections.abc import Iterable
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from functools import partial
from io import StringIO
from pathlib import Path
from time import monotonic

from more_itertools import intersperse
from rich.console import Console
from textual.app import App
from textual.pilot import Pilot

import spiel.constants
from spiel.app import SpielApp

ROOT_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT_DIR / "docs" / "assets"

# lie to Rich to make sure the screenshots are always generated in full color
os.environ["TERMCOLOR"] = "truecolor"


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
    await pilot.press(*intersperse("wait:50", keys), "wait:100")

    (ASSETS_DIR / name).with_suffix(".svg").write_text(take_reproducible_screenshot(pilot.app))

    await pilot.app.action_quit()


def take_screenshot(name: str, deck_file: Path, size: tuple[int, int], keys: Iterable[str]) -> str:
    print(f"Generating {name}")

    SpielApp(
        deck_path=deck_file,
        watch_path=deck_file.parent,
        show_messages=False,
        fixed_time=datetime(year=2022, month=12, day=17, hour=15, minute=31, second=42),
    ).run(
        headless=True,
        auto_pilot=partial(auto_pilot, name=name, keys=keys),
        size=size,
    )

    return name


if __name__ == "__main__":
    start_time = monotonic()

    demo_deck = spiel.constants.DEMO_FILE
    quickstart_deck = ROOT_DIR / "docs" / "examples" / "quickstart.py"
    slide_via_decorator = ROOT_DIR / "docs" / "examples" / "slide_via_decorator.py"
    slide_loop = ROOT_DIR / "docs" / "examples" / "slide_loop.py"
    triggers_reveal = ROOT_DIR / "docs" / "examples" / "triggers_reveal.py"
    triggers_animation = ROOT_DIR / "docs" / "examples" / "triggers_animation.py"

    with ProcessPoolExecutor() as pool:
        futures = [
            pool.submit(
                take_screenshot,
                name="triggers_animation_1",
                deck_file=triggers_animation,
                size=(70, 15),
                keys=(),
            ),
            pool.submit(
                take_screenshot,
                name="triggers_animation_2",
                deck_file=triggers_animation,
                size=(70, 15),
                keys=("wait:1450",),
            ),
            pool.submit(
                take_screenshot,
                name="triggers_animation_3",
                deck_file=triggers_animation,
                size=(70, 15),
                keys=("wait:2950",),
            ),
            pool.submit(
                take_screenshot,
                name="triggers_animation_4",
                deck_file=triggers_animation,
                size=(70, 15),
                keys=("wait:5450",),
            ),
            pool.submit(
                take_screenshot,
                name="demo",
                deck_file=demo_deck,
                size=(130, 35),
                keys=(),
            ),
            pool.submit(
                take_screenshot,
                name="deck",
                deck_file=demo_deck,
                size=(135, 40),
                keys=("d", "right", "down"),
            ),
            pool.submit(
                take_screenshot,
                name="help",
                deck_file=demo_deck,
                size=(110, 35),
                keys=("?",),
            ),
            pool.submit(
                take_screenshot,
                name="quickstart_basic",
                deck_file=quickstart_deck,
                size=(70, 20),
                keys=(),
            ),
            pool.submit(
                take_screenshot,
                name="quickstart_code",
                deck_file=demo_deck,
                size=(140, 45),
                keys=("right",),
            ),
            pool.submit(
                take_screenshot,
                name="slide_via_decorator",
                deck_file=slide_via_decorator,
                size=(60, 15),
                keys=(),
            ),
            pool.submit(
                take_screenshot,
                name="slide_loop_1",
                deck_file=slide_loop,
                size=(60, 15),
                keys=(),
            ),
            pool.submit(
                take_screenshot,
                name="slide_loop_2",
                deck_file=slide_loop,
                size=(60, 15),
                keys=("right",),
            ),
            pool.submit(
                take_screenshot,
                name="slide_loop_3",
                deck_file=slide_loop,
                size=(60, 15),
                keys=("right", "right"),
            ),
            pool.submit(
                take_screenshot,
                name="triggers_reveal_1",
                deck_file=triggers_reveal,
                size=(70, 15),
                keys=(),
            ),
            pool.submit(
                take_screenshot,
                name="triggers_reveal_2",
                deck_file=triggers_reveal,
                size=(70, 15),
                keys=("t",),
            ),
            pool.submit(
                take_screenshot,
                name="triggers_reveal_3",
                deck_file=triggers_reveal,
                size=(70, 15),
                keys=("t", "t"),
            ),
        ]

        for future in as_completed(futures, timeout=60):
            print(f"Generated {future.result()}")

    end_time = monotonic()

    print(f"Generated {len(futures)} screenshots in {end_time - start_time:0.2f} seconds")
