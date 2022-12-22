from __future__ import annotations

import asyncio
import code
import datetime
import importlib.util
import os
import sys
from asyncio import wait
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from functools import cached_property, partial
from pathlib import Path
from time import monotonic
from typing import Callable, ContextManager, Iterator, Optional

from rich.style import Style
from rich.text import Text
from textual import log
from textual.app import App
from textual.binding import Binding
from textual.events import Resize
from textual.reactive import reactive
from watchfiles import awatch

from spiel.constants import DECK, RELOAD_MESSAGE_TIME_FORMAT
from spiel.deck import Deck
from spiel.exceptions import NoDeckFound
from spiel.screens.deck import DeckScreen
from spiel.screens.help import HelpScreen
from spiel.screens.slide import SlideScreen
from spiel.triggers import Triggers
from spiel.utils import clamp
from spiel.widgets.slide import SlideWidget


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


SuspendType = Callable[[], ContextManager[None]]


class SpielApp(App[None]):
    CSS_PATH = "spiel.css"
    BINDINGS = [
        Binding("d", "switch_screen('deck')", "Go to the Deck view."),
        Binding("question_mark", "push_screen('help')", "Go to the Help view."),
        Binding("i", "repl", "Switch to the REPL."),
        Binding("p", "screenshot", "Take a screenshot."),
    ]

    deck = reactive(Deck(name="New Deck"))
    current_slide_idx = reactive(0)
    message = reactive(Text(""))

    def __init__(
        self,
        deck_path: Path,
        watch_path: Path,
        show_messages: bool = True,
        fixed_time: datetime.datetime | None = None,
    ):
        super().__init__()

        self.deck_path = deck_path
        self.watch_path = watch_path

        self.show_messages = show_messages
        self.fixed_time = fixed_time

    async def on_mount(self) -> None:
        self.deck = load_deck(self.deck_path)
        self.reloader = asyncio.create_task(self.reload())

        await self.install_screen(SlideScreen(), name="slide")
        await self.install_screen(DeckScreen(), name="deck")
        await self.install_screen(HelpScreen(), name="help")
        await self.push_screen("slide")

    async def reload(self) -> None:
        log(f"Watching {self.watch_path} for changes")
        async for changes in awatch(self.watch_path):
            change_msg = "\n  ".join([""] + [f"{k.raw_str()}: {v}" for k, v in changes])
            log(f"Reloading deck from {self.deck_path} due to detected file changes:{change_msg}")
            try:
                self.deck = load_deck(self.deck_path)
                self.current_slide_idx = clamp(self.current_slide_idx, 0, len(self.deck))
                self.set_message_temporarily(
                    Text(
                        f"Reloaded deck at {datetime.datetime.now().strftime(RELOAD_MESSAGE_TIME_FORMAT)}",
                        style=Style(dim=True),
                    ),
                    delay=10,
                )
            except Exception as e:
                self.set_message_temporarily(
                    Text(
                        f"Failed to reload deck at {datetime.datetime.now().strftime(RELOAD_MESSAGE_TIME_FORMAT)} due to: {e}",
                        style=Style(color="red"),
                    ),
                    delay=10,
                )

    def on_resize(self, event: Resize) -> None:
        self.set_message_temporarily(
            message=Text(f"Screen resized to {event.size}", style=Style(dim=True)), delay=2
        )

    def set_message_temporarily(self, message: Text, delay: float) -> None:
        if not self.show_messages:
            return

        self.message = message

        def clear() -> None:
            if self.message is message:
                self.message = Text("")

        self.set_timer(delay, clear)

    def action_next_slide(self) -> None:
        self.current_slide_idx = clamp(self.current_slide_idx + 1, 0, len(self.deck) - 1)

    def action_prev_slide(self) -> None:
        self.current_slide_idx = clamp(self.current_slide_idx - 1, 0, len(self.deck) - 1)

    def action_next_row(self) -> None:
        self.current_slide_idx = clamp(
            self.current_slide_idx + self.deck_grid_width, 0, len(self.deck) - 1
        )

    def action_prev_row(self) -> None:
        self.current_slide_idx = clamp(
            self.current_slide_idx - self.deck_grid_width, 0, len(self.deck) - 1
        )

    def watch_deck(self, new_deck: Deck) -> None:
        self.title = new_deck.name

    def watch_current_slide_idx(self, new_current_slide_idx: int) -> None:
        self.query_one(SlideWidget).triggers = Triggers.new()
        self.sub_title = self.deck[new_current_slide_idx].title

    def action_trigger(self) -> None:
        now = monotonic()
        slide_widget = self.query_one(SlideWidget)
        slide_widget.triggers = Triggers(now=now, times=(*slide_widget.triggers.times, now))

    def action_reset_trigger(self) -> None:
        slide_widget = self.query_one(SlideWidget)
        slide_widget.triggers = Triggers.new()

    @cached_property
    def repl(self) -> Callable[[], None]:
        # Lazily enable readline support
        import readline  # nopycln: import

        self.console.clear()  # clear the console the first time we go into the repl
        sys.stdout.flush()

        repl = code.InteractiveConsole()
        return partial(repl.interact, banner="", exitmsg="")

    def action_repl(self) -> None:
        with self.suspend():
            self.repl()

    async def action_quit(self) -> None:
        self.reloader.cancel()
        await wait([self.reloader], timeout=1)

        await super().action_quit()

    @contextmanager
    def suspend(self) -> Iterator[None]:
        driver = self._driver

        if driver is not None:
            driver.stop_application_mode()
            driver.exit_event.clear()  # type: ignore[attr-defined]
            with redirect_stdout(sys.__stdout__), redirect_stderr(sys.__stderr__):
                yield
            driver.start_application_mode()

    @property
    def deck_grid_width(self) -> int:
        return max(self.size.width // 35, 1)


def present(deck_path: Path | str, watch_path: Optional[Path | str] = None) -> None:
    """
    Present the deck defined in the given `deck_path`.

    Args:
        deck_path: The file to look for a deck in.
        watch_path: When filesystem changes are detected below this path (recursively), reload the deck from the `deck_path`.
    """
    os.environ["TEXTUAL"] = ",".join(sorted(["debug", "devtools"]))

    deck_path = Path(deck_path).resolve()
    watch_path = Path(watch_path or deck_path.parent).resolve()

    SpielApp(deck_path=deck_path, watch_path=watch_path).run()
