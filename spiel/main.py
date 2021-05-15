import shutil
from contextlib import nullcontext
from pathlib import Path
from textwrap import dedent

from rich.console import Console
from rich.control import Control
from rich.style import Style
from rich.syntax import Syntax
from rich.text import Text
from typer import Argument, Exit, Option, Typer

from .constants import PACKAGE_NAME, __version__
from .help import version_details
from .load import DeckWatcher
from .modes import Mode
from .present import present_deck
from .reloader import DeckReloader
from .state import State

THIS_DIR = Path(__file__).resolve().parent

app = Typer(
    help=dedent(
        f"""\
        Display richly-styled presentations using your terminal.

        To see what {PACKAGE_NAME.capitalize()} can do, take a look at the demo deck:

            $ spiel demo present

        A {PACKAGE_NAME.capitalize()} presentation (a "deck [of slides]") is defined programmatically using a Python script.
        """
    )
)


@app.command()
def present(
    path: Path = Argument(
        ...,
        dir_okay=False,
        help="The path to the slide deck file.",
    ),
    mode: Mode = Option(
        default=Mode.SLIDE,
        help="The mode to start presenting in.",
    ),
    slide: int = Option(
        default=1,
        help="The slide number to start the presentation on.",
    ),
    watch: bool = Option(
        default=False,
        help="If enabled, reload the deck when the slide deck file changes.",
    ),
    poll: bool = Option(
        default=False,
        help="If enabled, poll the filesystem for changes (implies --watch). Use this option on systems that don't support file modification notifications.",
    ),
) -> None:
    """
    Present a deck.
    """
    _present(path=path, mode=mode, slide=slide, watch=watch, poll=poll)


def _present(path: Path, mode: Mode, slide: int, watch: bool, poll: bool) -> None:
    console = Console()

    try:
        state = State.from_file(path)
    except FileNotFoundError as e:
        console.print(Text(f"Error: {e}", style=Style(color="red")))
        raise Exit(code=1)

    state.mode = mode
    state.jump_to_slide(slide - 1)

    watcher = (
        DeckWatcher(event_handler=DeckReloader(state, path), path=path, poll=poll)
        if (watch or poll)
        else nullcontext()
    )

    try:
        with state, watcher:
            present_deck(state)
    except KeyboardInterrupt:
        raise Exit(code=0)
    finally:
        state.console.print(Control.clear())
        state.console.print(Control.move_to(0, 0))


@app.command()
def init(
    path: Path = Argument(
        ...,
        writable=True,
        resolve_path=True,
        help="The path to create a new deck script at.",
    )
) -> None:
    """
    Create a new deck script at the given path from a basic template.

    This is a good starting point if you already know what you want to do.
    If you're not so sure, consider taking a look at the demo deck to see what's possible:

        $ spiel demo --help
    """
    console = Console()

    if path.exists():
        console.print(
            Text(f"Error: {path} already exists, refusing to overwrite.", style=Style(color="red"))
        )
        raise Exit(code=1)

    name = path.stem.replace("_", " ").title()

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        console.print(
            Text(
                f"Error: was not able to ensure that the parent directory {path.parent} exists due to: {e}.",
                style=Style(color="red"),
            )
        )
        raise Exit(code=1)

    try:
        path.write_text(
            dedent(
                f"""\
                from textwrap import dedent

                from spiel import Deck, Options

                deck = Deck(name="{name}")
                options = Options()

                @deck.slide(title="Title")
                def title():
                    markup = dedent(
                        \"""\\
                        # {name}

                        This is your title slide!
                        \"""
                    )

                    return Markdown(markup, justify="center")
                """
            )
        )
    except Exception as e:
        console.print(
            Text(
                f"Error: was not able to write template to {path} due to: {e}",
                style=Style(color="red"),
            )
        )
        raise Exit(code=1)

    console.print(Text(f"Wrote deck template to {path}", style=Style(color="green")))


@app.command()
def version(
    plain: bool = Option(
        default=False,
        help=f"Print only {PACKAGE_NAME}'s version.",
    )
) -> None:
    """
    Display version and debugging information.
    """
    console = Console()

    if plain:
        print(__version__)
    else:
        console.print(version_details(console))


demo = Typer(
    name="demo",
    help=dedent(
        """\
        Use the demonstration deck (present it, display source, etc.).
        """
    ),
)

DEMO_DIR = THIS_DIR / "demo"
DEMO_SOURCE = THIS_DIR / "demo" / "demo.py"


@demo.command(name="present")
def present_demo() -> None:
    """
    Present the demo deck.
    """
    _present(path=DEMO_SOURCE, mode=Mode.SLIDE, slide=0, watch=False, poll=False)


@demo.command()
def source() -> None:
    """
    Display the source code for the demo deck in your PAGER.
    """
    console = Console()

    with console.pager(styles=True):
        console.print(Syntax(DEMO_SOURCE.read_text(), lexer_name="python"))


@demo.command()
def copy(
    path: Path = Argument(
        default=...,
        writable=True,
        help="The path to copy the demo deck source code and assets to.",
    )
) -> None:
    """
    Copy the demo deck source code and assets to a new directory.

    If you're looking for a more stripped-down starting point, try the init command:

        $ spiel init --help
    """
    console = Console()

    if path.exists():
        console.print(Text(f"Error: {path} already exists!", style=Style(color="red")))
        raise Exit(code=2)

    try:
        shutil.copytree(DEMO_DIR, path)
    except Exception as e:
        console.print(Text(f"Failed to copy demo deck directory: {e}", style=Style(color="red")))
        raise Exit(code=1)

    console.print(
        Text(f"Wrote demo deck source code and assets to {path}", style=Style(color="green"))
    )


app.add_typer(demo)
