import os
import shutil
from pathlib import Path
from textwrap import dedent

from click.exceptions import Exit
from rich.console import Console
from rich.style import Style
from rich.syntax import Syntax
from rich.text import Text
from typer import Argument, Option, Typer

from spiel.app import SpielApp
from spiel.constants import DEMO_DIR, DEMO_FILE, PACKAGE_DIR, PACKAGE_NAME, __version__
from spiel.renderables.debug import DebugTable

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


@cli.command()
def present(
    path: Path = Argument(
        ...,
        dir_okay=False,
        exists=True,
        readable=True,
        help="The path to the slide deck file.",
    ),
    watch: Path = Option(
        default=Path.cwd(),
    ),
) -> None:
    """
    Present a deck.
    """
    _present(deck_path=path, watch_path=watch)


def _present(deck_path: Path, watch_path: Path) -> None:
    os.environ["TEXTUAL"] = ",".join(sorted(["debug", "devtools"]))

    app = SpielApp(deck_path=deck_path, watch_path=watch_path)
    app.run()


@cli.command()
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
                from spiel import Deck


                deck = Deck(name="{name}")

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
    _present(deck_path=DEMO_FILE, watch_path=PACKAGE_DIR)


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
    )
) -> None:
    """
    Display version and debugging information.
    """

    if plain:
        console.print(__version__, style=Style())
    else:
        console.print(DebugTable())
