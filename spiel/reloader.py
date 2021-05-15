import sys
from dataclasses import dataclass, field
from pathlib import Path

from pendulum import DateTime, now
from rich.control import Control
from rich.style import Style
from rich.text import Text
from watchdog.events import FileSystemEvent, FileSystemEventHandler

from .load import load_deck_and_options
from .state import State


@dataclass
class DeckReloader(FileSystemEventHandler):
    state: State
    deck_path: Path
    last_reload: DateTime = field(default_factory=now)

    def on_modified(self, event: FileSystemEvent) -> None:
        self.last_reload = now()
        try:
            self.state.deck, _ = load_deck_and_options(self.deck_path)
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
