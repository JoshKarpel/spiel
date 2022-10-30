from __future__ import annotations

import asyncio
import datetime
import importlib.util
import sys
from asyncio import wait
from pathlib import Path
from typing import Type

from rich.style import Style
from rich.text import Text
from textual import log
from textual.app import App, CSSPathType
from textual.binding import Binding
from textual.driver import Driver
from textual.reactive import reactive
from watchfiles import awatch

from spiel.constants import DECK, RELOAD_MESSAGE_TIME_FORMAT
from spiel.deck import Deck, Slide
from spiel.exceptions import NoDeckFound
from spiel.screens.deck import DeckScreen
from spiel.screens.help import HelpScreen
from spiel.screens.slide import SlideScreen
from spiel.utils import clamp
from spiel.widgets.footer import Footer


def load_deck(path: Path) -> Deck:
    module_name = "__deck"
    spec = importlib.util.spec_from_file_location(module_name, path)

    if spec is None:
        raise NoDeckFound(f"{path.resolve()} does not appear to be an importable Python module.")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module

    loader = spec.loader
    assert loader is not None
    loader.exec_module(module)

    try:
        deck = getattr(module, DECK)
    except AttributeError:
        raise NoDeckFound(f"The module at {path} does not have an attribute named {DECK}.")

    if not isinstance(deck, Deck):
        raise NoDeckFound(
            f"The module at {path} has an attribute named {DECK}, but it is a {type(deck).__name__}, not a {Deck.__name__}."
        )

    return deck


class SpielApp(App[None]):
    CSS_PATH = "spiel.css"
    BINDINGS = [
        Binding("ctrl+d", "toggle_dark", "Toggle dark mode"),
        Binding("right", "next_slide", "Next Slide"),
        Binding("left", "prev_slide", "Previous Slide"),
        Binding("d", "push_screen('deck')", "Deck View"),
        Binding("question_mark", "push_screen('help')", "Help"),
    ]
    SCREENS = {"deck": DeckScreen(), "help": HelpScreen()}

    slide_idx = reactive(0)
    message = reactive("")

    def __init__(
        self,
        deck: Deck,
        deck_path: Path,
        watch_path: Path,
        driver_class: Type[Driver] | None = None,
        css_path: CSSPathType = None,
        watch_css: bool = False,
    ):
        super().__init__(driver_class=driver_class, css_path=css_path, watch_css=watch_css)

        self.deck = deck
        self.deck_path = deck_path
        self.watch_path = watch_path

    def on_mount(self) -> None:
        self.reloader = asyncio.create_task(self.reload())

        self.push_screen(SlideScreen())

    async def reload(self) -> None:
        log(f"Watching {self.watch_path} for changes")
        async for changes in awatch(self.watch_path):
            log(f"Reloading due to changes: {changes}")
            self.deck = load_deck(self.deck_path)
            self.slide_idx = clamp(self.slide_idx, 0, len(self.deck))
            for footer in self.query(Footer):
                footer.message = Text(
                    f"Reloaded deck at {datetime.datetime.now().strftime(RELOAD_MESSAGE_TIME_FORMAT)}",
                    style=Style(italic=True, color="cyan"),
                )

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_next_slide(self) -> None:
        self.slide_idx = clamp(self.slide_idx + 1, 0, len(self.deck) - 1)

    def action_prev_slide(self) -> None:
        self.slide_idx = clamp(self.slide_idx - 1, 0, len(self.deck) - 1)

    @property
    def current_slide(self) -> Slide:
        return self.deck.slides[self.slide_idx]

    async def action_quit(self) -> None:
        self.reloader.cancel()
        await wait([self.reloader], timeout=1)

        await super().action_quit()