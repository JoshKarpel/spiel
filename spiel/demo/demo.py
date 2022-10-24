import inspect
import shutil
import socket
from datetime import datetime
from pathlib import Path
from textwrap import dedent

from rich.align import Align
from rich.box import SQUARE
from rich.console import Group
from rich.layout import Layout
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.style import Style
from rich.syntax import Syntax
from rich.text import Text

from spiel import __version__
from spiel.app import Deck, Slide

deck = Deck(name=f"Spiel Demo Deck (v{__version__})")

SPIEL = "[Spiel](https://github.com/JoshKarpel/spiel)"
RICH = "[Rich](https://rich.readthedocs.io/)"
IPYTHON = "[IPython](https://ipython.readthedocs.io)"
WSL = "[Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/)"

THIS_DIR = Path(__file__).resolve().parent


@deck.slide(title="What is Spiel?")
def what():
    upper_left_markup = dedent(
        f"""\
        ## What is Spiel?

        {SPIEL} is a framework for building and presenting richly-styled presentations in your terminal using Python.

        Spiel uses {RICH} to render slide content.
        Anything you can display with Rich, you can display with Spiel (plus some other things)!

        Use your right `→` and left `←` arrows keys (or `f` and `b`) to go forwards and backwards through the deck.

        Press `ctrl-c` or `ctrl-k` to exit.

        Press `h` at any time to see the help screen, which describes all of the actions you can take.

        To get a copy of the source code for this deck, use the `spiel demo copy` command.
        """
    )

    upper_right_markup = dedent(
        """\
        ## Why use Spiel?

        It's fun!

        It's weird!

        Why not?

        Maybe you shouldn't.

        Honestly, it's unclear whether it's a good idea.

        There's always [Powerpoint](https://youtu.be/uNjxe8ShM-8)!
        """
    )

    lower_left_markup = dedent(
        f"""\
        ## Contributing

        Please report bugs via [GitHub Issues](https://github.com/JoshKarpel/spiel/issues).

        If you have ideas about how Spiel can be improved,
        or you have a cool deck to show off,
        please post to [GitHub Discussions](https://github.com/JoshKarpel/spiel/discussions).
        """
    )

    lower_right_markup = dedent(
        f"""\
        ## Inspirations

        Brandon Rhodes' [PyCon 2017](https://youtu.be/66P5FMkWoVU) and [North Bay Python 2017](https://youtu.be/rrMnmLyYjU8) talks.

        David Beazley's [Lambda Calculus from the Ground Up](https://youtu.be/pkCLMl0e_0k) tutorial at PyCon 2019.

        LaTeX's [Beamer](https://ctan.org/pkg/beamer) document class.
        """
    )

    def pad_markdown(markup):
        return Padding(Markdown(markup, justify="center"), pad=(0, 5))

    root = Layout()
    upper = Layout()
    lower = Layout()

    upper.split_row(
        Layout(pad_markdown(upper_left_markup)),
        Layout(pad_markdown(upper_right_markup)),
    )
    lower.split_row(
        Layout(pad_markdown(lower_left_markup)),
        Layout(pad_markdown(lower_right_markup)),
    )
    root.split_column(upper, lower)

    return root


@deck.slide(title="Decks and Slides")
def code():
    markup = dedent(
        f"""\
    ## Decks are made of Slides

    Here's the code for `Deck` and `Slide`!

    The source code is pulled directly from the definitions via [inspect.getsource](https://docs.python.org/3/library/inspect.html#inspect.getsource).

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
                lexer="python",
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


@deck.slide(title="Dynamic Content", dynamic=True)
def dynamic():
    home = Path.home()
    width = shutil.get_terminal_size().columns
    width_limit = 80
    home_dir_contents = list(home.iterdir())
    return Group(
        Align.center(
            Text(
                f"Slides can have dynamic content!",
                style=Style(color="bright_magenta", bold=True, italic=True),
                justify="center",
            ),
        ),
        Align.center(
            Panel(
                Text(
                    f"Your terminal is {width} cells wide"
                    if width > width_limit
                    else f"Your terminal is only {width} cells wide! Get a bigger monitor!",
                    style=Style(color="green1" if width > width_limit else "red"),
                    justify="center",
                )
            ),
        ),
        Align.center(
            Panel(
                Text.from_markup(
                    f"The time on this computer ([bold]{socket.gethostname()}[/bold]) is {datetime.now()}",
                    style="bright_cyan",
                    justify="center",
                )
            ),
        ),
        Align.center(
            Panel(
                Text(
                    f"There are {len([f for f in home_dir_contents if f.is_file()])} files and {len([f for f in home_dir_contents if f.is_dir()])} directories in {home}",
                    style=Style(color="yellow"),
                    justify="center",
                )
            ),
        ),
    )
