from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass, field
from pathlib import Path
from types import TracebackType
from typing import ContextManager, Optional, Type

from pendulum import DateTime, now
from rich.control import Control
from rich.style import Style
from rich.text import Text
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver

from spiel.constants import DECK
from spiel.exceptions import NoDeckFound
from spiel.slides import Deck
from spiel.state import State


def load_deck(deck_path: Path) -> Deck:
    module_name = "__deck"
    spec = importlib.util.spec_from_file_location(module_name, deck_path)

    if spec is None:
        raise FileNotFoundError(f"{deck_path} does not appear to be an importable Python module.")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)  # type: ignore

    try:
        return getattr(module, DECK)
    except AttributeError as e:
        raise NoDeckFound(f"The module at {deck_path} does not have an attribute named {DECK}.")


@dataclass
class DeckReloader(FileSystemEventHandler):
    state: State
    deck_path: Path
    last_reload: DateTime = field(default_factory=now)

    def on_modified(self, event: FileSystemEvent) -> None:
        self.last_reload = now()
        try:
            self.state.deck = load_deck(self.deck_path)
            self.state.reset_trigger()
            self.state.set_message(
                lambda: Text(
                    f"Reloaded deck from {self.deck_path} {self.last_reload.diff_for_humans(None, False)}",
                    style=Style(color="bright_green"),
                )
            )
        except Exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.state.set_message(
                lambda: Text(
                    f"Error: {self.last_reload.diff_for_humans(None, False)}: {exc_obj!r}{Control.bell()}",
                    style=Style(color="bright_red"),
                )
            )

    def __hash__(self) -> int:
        return hash((type(self), id(self)))


@dataclass
class DeckWatcher(ContextManager):
    event_handler: FileSystemEventHandler
    path: Path
    poll: bool = False

    def __post_init__(self) -> None:
        self.observer = (PollingObserver if self.poll else Observer)(timeout=0.1)

    def __enter__(self) -> DeckWatcher:
        self.observer.schedule(self.event_handler, str(self.path))
        self.observer.start()

        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        self.observer.stop()
        self.observer.join()

        return None
