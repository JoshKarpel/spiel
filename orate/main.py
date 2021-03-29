import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path

from rich.console import Console
from typer import Argument, Option, Typer
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver

from orate.display import display_deck
from orate.slides import Deck
from orate.state import State

app = Typer()
console = Console()


def load_deck(deck_path: Path) -> Deck:
    module_name = "__deck"
    spec = importlib.util.spec_from_file_location(module_name, deck_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return getattr(module, "DECK")


@dataclass
class DeckReloader(FileSystemEventHandler):
    state: State
    deck_path: Path

    def on_modified(self, event: FileSystemEvent) -> None:
        self.state.deck = load_deck(self.deck_path)

    def __hash__(self) -> int:
        return hash((type(self), id(self)))


@app.command()
def display(
    path: Path = Argument(..., help="The path to the slide deck file."),
    watch: bool = Option(
        default=False, help="If enabled, reload the deck when the slide deck file changes."
    ),
    poll: bool = Option(
        default=False,
        help="If enabled, poll the filesystem for changes (implies --watch). Use this option on systems that don't support file modification notifications.",
    ),
) -> None:
    state = State(deck=load_deck(path))
    watch = watch or poll

    if watch:
        event_handler = DeckReloader(state, path)
        observer = PollingObserver() if poll else Observer()
        observer.schedule(event_handler, str(path))
        observer.start()

    try:
        display_deck(console, state)
    finally:
        if watch:
            observer.stop()
            observer.join()
