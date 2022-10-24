import os
from pathlib import Path
from textwrap import dedent

from typer import Argument, Option, Typer

from spiel.app import SpielApp
from spiel.constants import PACKAGE_NAME

cli = Typer(
    name=PACKAGE_NAME,
    no_args_is_help=True,
    rich_markup_mode="rich",
    help=dedent(
        f"""\
        Display [italic yellow]Rich[/italic yellow]ly-styled presentations using your terminal.

        To see what {PACKAGE_NAME.capitalize()} can do, take a look at the demo deck:

            $ spiel demo present

        A {PACKAGE_NAME.capitalize()} presentation (a "[italic green]deck[/italic green] of slides") is defined programmatically using a Python script.
        """
    ),
)


@cli.command()
def present(
    path: Path = Argument(
        ...,
        dir_okay=False,
        help="The path to the slide deck file.",
    ),
    watch: Path = Option(
        default=Path.cwd(),
    ),
) -> None:
    """
    Present a deck.
    """
    _present(path=path, watch=watch)


def _present(path: Path, watch: Path) -> None:
    os.environ["TEXTUAL"] = ",".join(sorted(["debug", "devtools"]))
    app = SpielApp(path=path, watch=watch)
    app.run()
