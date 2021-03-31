import inspect
import shutil
import socket
from datetime import datetime
from pathlib import Path
from textwrap import dedent

from rich.align import Align
from rich.box import SQUARE
from rich.console import RenderGroup
from rich.layout import Layout
from rich.markdown import Markdown
from rich.panel import Panel
from rich.style import Style
from rich.syntax import Syntax
from rich.text import Text

from spiel import Deck, Slide, __version__

SPIEL = "[Spiel](https://github.com/JoshKarpel/spiel)"
RICH = "[Rich](https://rich.readthedocs.io/)"


DECK = Deck(name=f"Spiel Demo Deck (v{__version__})")


@DECK.slide(title="What is Spiel?")
def what():
    left_markup = dedent(
        f"""\
    ## What is Spiel?

    {SPIEL} is a framework for building slide decks in Python.

    Spiel uses {RICH} to render slide content.

    Anything you can display with Rich, you can display with Spiel!
    """
    )

    right_markup = dedent(
        """\
    ## Why use Spiel?

    It's fun!

    It's weird!
    """
    )

    r = 3
    root = Layout()
    root.split_row(
        Layout(
            Markdown(
                left_markup,
                justify="center",
            ),
            ratio=r,
        ),
        Layout(" "),
        Layout(
            Markdown(
                right_markup,
                justify="center",
            ),
            ratio=r,
        ),
    )

    return root


@DECK.slide(title="Decks and Slides")
def code():
    markup = dedent(
        f"""\
    ## Decks are made of Slides

    Here's the code for `Deck` and `Slide`!

    The source code is pulled directly from the definitions via [`inspect.getsource`](https://docs.python.org/3/library/inspect.html#inspect.getsource).

    ({RICH} supports syntax highlighting, so {SPIEL} does too!)
    """
    )
    root = Layout()
    upper = Layout(Markdown(markup, justify="center"), size=len(markup.split("\n")) + 1)
    lower = Layout()
    root.split_column(upper, lower)

    def make_code_panel(obj):
        lines, line_number = inspect.getsourcelines(obj)
        return Panel(
            Syntax(
                "".join(lines),
                lexer_name="python",
                line_numbers=True,
                start_line=line_number,
            ),
            box=SQUARE,
            border_style=Style(dim=True),
            height=len(lines) + 2,
        )

    lower.split_row(
        Layout(make_code_panel(Deck)),
        Layout(make_code_panel(Slide)),
    )

    return root


@DECK.slide(title="Dynamic Content", dynamic=True)
def dynamic():
    home = Path.home()
    width = shutil.get_terminal_size().columns
    width_limit = 80
    return RenderGroup(
        Align(
            Text(
                f"Slides can have dynamic content!",
                style=Style(color="bright_magenta", bold=True, italic=True),
                justify="center",
            ),
            align="center",
        ),
        Align(
            Panel(
                Text(
                    f"Your terminal is {width} characters wide."
                    if width > width_limit
                    else f"Your terminal is only {width} characters wide! Get a bigger monitor!",
                    style=Style(color="green1" if width > width_limit else "red"),
                    justify="center",
                )
            ),
            align="center",
        ),
        Align(
            Panel(
                Text(
                    f"The time on this computer, {socket.gethostname()}, is {datetime.now()}",
                    style=Style(color="bright_cyan", bold=True, italic=True),
                    justify="center",
                )
            ),
            align="center",
        ),
        Align(
            Panel(
                Text(
                    f"There are {len([f for f in home.iterdir() if f.is_file()])} files in {home} right now.",
                    style=Style(color="yellow"),
                    justify="center",
                )
            ),
            align="center",
        ),
    )


@DECK.slide(title="Views")
def grid():
    markup = dedent(
        """\
    ## Multiple Views

    Try pressing 'd' to go into "deck" view.
    Press 's' to go back to "slide" view.
    """
    )
    return Markdown(markup, justify="center")


@DECK.slide(title="Watch Mode")
def watch():
    markup = dedent(
        f"""\
    ## Developing a Deck

    {SPIEL} can reload your deck as you edit it if you add the `--watch` option to `display`:

    `$ spiel display examples/demo.py --watch`

    If you're on a system without inotify support (e.g., Windows Subsystem for Linux), you may need to use the `--poll` option instead.

    When you're ready to present your deck for real, just drop the `--watch` option.
    """
    )
    return Markdown(markup, justify="center")
