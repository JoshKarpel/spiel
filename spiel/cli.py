import shutil
from pathlib import Path
from textwrap import dedent
from typing import Optional

import typer.rich_utils as ru
from click.exceptions import Exit
from rich.console import Console
from rich.style import Style
from rich.syntax import Syntax
from rich.text import Text
from typer import Argument, Option, Typer

from spiel.app import present
from spiel.constants import DEMO_DIR, DEMO_FILE, PACKAGE_DIR, PACKAGE_NAME, __version__
from spiel.renderables.debug import DebugTable

ru.STYLE_HELPTEXT = ""

console = Console()


cli = Typer(
    name=PACKAGE_NAME,
    no_args_is_help=True,
    rich_markup_mode="rich",
    help=dedent(
        f"""\
        Display [italic yellow]Rich[/italic yellow]ly-styled presentations using your terminal.

        To see what {PACKAGE_NAME.capitalize()} can do, take a look at the demo deck:

            $ spiel demo present

        A {PACKAGE_NAME.capitalize()} presentation (a "[italic green]deck[/italic green] of slides")
        is defined programmatically using a Python script.
        """
    ),
)


@cli.command(name="present")
def _present(
    path: Path = Argument(
        ...,
        dir_okay=False,
        exists=True,
        readable=True,
        help="The path to the slide deck file.",
    ),
    watch: Optional[Path] = Option(
        default=None,
        help="When filesystem changes are detected below this path (recursively), reload the deck from the deck path. Defaults to the parent directory of the deck path.",
    ),
) -> None:
    """
    Present a deck.
    """
    present(deck_path=path, watch_path=watch)


demo = Typer(
    name="demo",
    no_args_is_help=True,
    rich_markup_mode="rich",
    help=dedent(
        """\
        Use the demonstration deck (present it, display source, etc.).
        """
    ),
)
cli.add_typer(demo)


@demo.command(name="present")
def present_demo() -> None:
    """
    Present the demo deck.
    """
    present(deck_path=DEMO_FILE, watch_path=PACKAGE_DIR)


@demo.command()
def source() -> None:
    """
    Display the source code for the demo deck in your PAGER.
    """
    console = Console()

    with console.pager(styles=True):
        console.print(Syntax(DEMO_FILE.read_text(encoding="utf-8"), lexer="python"))


@demo.command()
def copy(
    path: Path = Argument(
        default=...,
        exists=False,
        writable=True,
        help="The path to copy the demo deck source code and assets to.",
    ),
) -> None:
    """
    Copy the demo deck source code and assets to a new directory.

    If you're looking for a more stripped-down starting point, try the init command:
        $ spiel init --help
    """
    console = Console()

    if path.exists():
        console.print(Text(f"Error: {path} already exists!", style=Style(color="red")))
        raise Exit(code=1)

    try:
        shutil.copytree(DEMO_DIR, path)
    except Exception as e:
        console.print(Text(f"Failed to copy demo deck directory: {e}", style=Style(color="red")))
        raise Exit(code=1)

    console.print(
        Text(f"Wrote demo deck source code and assets to {path}", style=Style(color="green"))
    )


@cli.command()
def version(
    plain: bool = Option(
        default=False,
        help=f"Print only {PACKAGE_NAME}'s version.",
    ),
) -> None:
    """
    Display version and debugging information.
    """

    if plain:
        console.print(Text(__version__))
    else:
        console.print(DebugTable())
