import inspect
import os
import shutil
import socket
import tempfile
from datetime import datetime
from textwrap import dedent

from rich.align import Align
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

    return Slide(root, title="What is Spiel?")


def code():
    markup = dedent(
        f"""\
    ## Decks are made of Slides

    Here's the code for `Deck` and `Slide`!

    The source code is pulled directly from the definitions via [`inspect.getsource`](https://docs.python.org/3/library/inspect.html#inspect.getsource).

    (Because {RICH} supports syntax highlighting, so does {SPIEL}!)
    """
    )
    root = Layout()
    upper = Layout(Markdown(markup, justify="center"), size=len(markup.split("\n")) + 1)
    lower = Layout()
    root.split_column(upper, lower)

    lower.split_row(
        Layout(
            Syntax(
                inspect.getsource(Deck),
                lexer_name="python",
            ),
        ),
        Layout(
            Syntax(
                inspect.getsource(Slide),
                lexer_name="python",
            ),
        ),
    )

    return Slide(root, title="Decks and Slides")


def dynamic():
    tmp_dir = tempfile.gettempdir()
    width = shutil.get_terminal_size().columns
    return Slide(
        RenderGroup(
            Align(
                Text(
                    f"Your slides can have very dynamic content, like this!",
                    style=Style(color="bright_magenta", bold=True, italic=True),
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
                        f"Your terminal is {width} characters wide."
                        if width > 80
                        else f"Your terminal is only {width} characters wide! Get a bigger monitor!",
                        style=Style(color="green1" if width > 80 else "red"),
                        justify="center",
                    )
                ),
                align="center",
            ),
            Align(
                Panel(
                    Text(
                        f"There are {len(os.listdir(tmp_dir))} entries under {tmp_dir} right now.",
                        style=Style(color="yellow"),
                        justify="center",
                    )
                ),
                align="center",
            ),
        ),
        title="Dynamic Content",
    )


def grid():
    markup = dedent(
        """\
    ## Multiple Views

    Try pressing 'd' to go into "deck" view.
    Press 's' to go back to "slide" view.
    """
    )
    return Slide(Markdown(markup, justify="center"), title="Views")


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
    return Slide(Markdown(markup, justify="center"), title="Watch Mode")


DECK = Deck(name=f"Spiel Demo Deck (v{__version__})").add_slides(
    what(),
    code(),
    dynamic,
    grid(),
    watch(),
)
