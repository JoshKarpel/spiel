from contextlib import nullcontext
from pathlib import Path

from rich.console import Console
from typer import Argument, Option, Typer

from spiel.present import present_deck
from spiel.state import State
from spiel.load import DeckReloader, load_deck, DeckWatcher

app = Typer()
console = Console()


@app.command()
def present(
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

    watcher = (
        DeckWatcher(event_handler=DeckReloader(state, path), path=path, poll=poll)
        if (watch or poll)
        else nullcontext()
    )

    with watcher:
        present_deck(console, state)
