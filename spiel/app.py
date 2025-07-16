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
from typing import Callable, ClassVar, ContextManager, Iterator, List, Tuple

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
from spiel.screens.transition import SlideTransitionScreen
from spiel.transitions.protocol import Direction
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
    BINDINGS: ClassVar[List[Binding | Tuple[str, str, str]]] = [
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
        watch_path: Path | None = None,
        _show_messages: bool = True,
        _fixed_time: datetime.datetime | None = None,
        _fixed_triggers: Triggers | None = None,
        _enable_transitions: bool = True,
        _slide_refresh_rate: float = 1 / 60,
    ) -> None:
        super().__init__()

        self.deck_path = deck_path
        self.watch_path = watch_path

        self.show_messages = _show_messages
        self.fixed_time = _fixed_time
        self.fixed_triggers = _fixed_triggers
        self.enable_transitions = _enable_transitions
        self.slide_refresh_rate = _slide_refresh_rate

    async def on_mount(self) -> None:
        self.deck = load_deck(self.deck_path)
        self.reloader = asyncio.create_task(self.reload())

        self.install_screen(SlideScreen(), name="slide")
        self.install_screen(DeckScreen(), name="deck")
        self.install_screen(HelpScreen(), name="help")
        await self.push_screen("slide")

    async def reload(self) -> None:
        if self.watch_path is None:
            return

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

    async def action_next_slide(self) -> None:
        await self.handle_new_slide(self.current_slide_idx + 1, Direction.Next)

    async def action_prev_slide(self) -> None:
        await self.handle_new_slide(self.current_slide_idx - 1, Direction.Previous)

    async def handle_new_slide(self, new_slide_idx: int, direction: Direction) -> None:
        new_slide_idx = clamp(new_slide_idx, 0, len(self.deck) - 1)

        current_slide = self.deck[self.current_slide_idx]
        new_slide = self.deck[new_slide_idx]

        transition = new_slide.transition or self.deck.default_transition

        if (
            self.current_slide_idx == new_slide_idx
            or not isinstance(self.screen, SlideScreen)
            or transition is None
            or not self.enable_transitions
        ):
            self.current_slide_idx = new_slide_idx
            return

        transition_screen = SlideTransitionScreen(
            from_slide=current_slide,
            from_triggers=self.query_one(SlideWidget).triggers,
            to_slide=new_slide,
            direction=direction,
            transition=transition,
        )
        await self.switch_screen(transition_screen)
        transition_screen.animate(
            "progress",
            value=100,
            delay=0,
            duration=0.75,
            on_complete=lambda: self.finalize_transition(new_slide_idx),
        )

    async def finalize_transition(self, new_slide_idx: int) -> None:
        await self.switch_screen("slide")

        self.current_slide_idx = new_slide_idx

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
        self.query_one(SlideWidget).triggers = self.fixed_triggers or Triggers.new()
        self.sub_title = self.deck[new_current_slide_idx].title

    def action_trigger(self) -> None:
        now = monotonic()
        slide_widget = self.query_one(SlideWidget)
        slide_widget.triggers = Triggers(now=now, _times=(*slide_widget.triggers._times, now))

    def action_reset_trigger(self) -> None:
        slide_widget = self.query_one(SlideWidget)
        slide_widget.triggers = Triggers.new()

    @cached_property
    def repl(self) -> Callable[[], None]:
        # Lazily enable readline support
        try:
            import readline  # noqa: F401, PLC0415
        except ImportError:
            pass

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
            with redirect_stdout(sys.__stdout__), redirect_stderr(sys.__stderr__):
                yield
            driver.start_application_mode()

    @property
    def deck_grid_width(self) -> int:
        return max(self.size.width // 35, 1)


def present(deck_path: Path | str, watch_path: Path | str | None = None) -> None:
    """
    Present the deck defined in the given `deck_path`.

    Args:
        deck_path: The file to look for a deck in.
        watch_path: When filesystem changes are detected below this path (recursively), reload the deck from the `deck_path`.
            If `None` (the default), use the parent directory of the `deck_path`.
    """
    os.environ["TEXTUAL"] = ",".join(sorted({"debug", "devtools"}))

    deck_path = Path(deck_path).resolve()
    watch_path = Path(watch_path or deck_path.parent).resolve()

    SpielApp(deck_path=deck_path, watch_path=watch_path).run()
