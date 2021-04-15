import inspect
import shutil
import socket
from datetime import datetime
from math import cos, floor, pi
from pathlib import Path
from textwrap import dedent

import os
from rich.align import Align
from rich.box import SQUARE
from rich.color import Color, blend_rgb
from rich.console import RenderGroup
from rich.layout import Layout
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.style import Style
from rich.syntax import Syntax
from rich.text import Text

from spiel import Deck, Image, Slide, __version__
from spiel.example import Example

SPIEL = "[Spiel](https://github.com/JoshKarpel/spiel)"
RICH = "[Rich](https://rich.readthedocs.io/)"


DECK = Deck(name=f"Spiel Demo Deck (v{__version__})")

THIS_DIR = Path(__file__).resolve().parent


DECK.add_slides(
    Example(
        source=f"""\
# This is an example showing how to use random.choice from the standard library.

# The source code is embedded directly into the demo deck file, 
# but you could load it from another file if you wanted to.

# Press t (same as trigger) to execute the example code and display the output.

# Press e to open your $EDITOR ({os.getenv('EDITOR', 'not set')}) on the example code.
# Save your changes and exit to come back to the presentation with your updated code.

import random

directions = ["North", "South", "East", "West"]

print("Which way should we go?")
print(random.choice(directions))
""",
        title="Examples",
    ),
)


@DECK.slide(title="What is Spiel?")
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

        If you have ideas about how Spiel can be improved or a cool deck to show off,
        please post them via [GitHub Discussions](https://github.com/JoshKarpel/spiel/discussions).
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


@DECK.slide(title="Dynamic Content")
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
                    f"Your terminal is {width} cells wide."
                    if width > width_limit
                    else f"Your terminal is only {width} cells wide! Get a bigger monitor!",
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


@DECK.slide(title="Triggers")
def triggers(triggers):
    info = Markdown(
        dedent(
            f"""\
            ## Triggers

            Triggers are a mechanism for making dynamic content that depends on *relative* time.

            Triggers can be used to implement effects like fades, motion, and other "animated" effects.

            Each slide is triggered once when it starts being displayed.
            You can trigger it again (as many times as you'd like) by pressing `t`.
            You can reset the trigger state by pressing `r`.

            This slide has been triggered {len(triggers)} times.
            It was last triggered {triggers.time_since_last_trigger:.2f} seconds ago.
            """
        ),
        justify="center",
    )

    bounce_period = 10
    width = 50
    half_width = width // 2

    bounce_time = triggers.time_since_first_trigger % bounce_period
    bounce_character = "⁍" if bounce_time < (1 / 2) * bounce_period else "⁌"
    bounce_position = floor(half_width * cos(2 * pi * bounce_time / bounce_period))
    before = half_width + bounce_position
    ball = Align.center(
        Panel(
            Padding(
                bounce_character,
                pad=(0, before, 0, (half_width - bounce_position - 1)),
            ),
            title="Bouncing Bullet",
            padding=0,
        )
    )

    white = Color.parse("bright_white")
    black = Color.parse("black")
    red = Color.parse("bright_red")
    green = Color.parse("bright_green")

    fade_time = 3

    lines = [
        Text(
            "Triggered!",
            style=Style(
                color=(
                    Color.from_triplet(
                        blend_rgb(
                            black.get_truecolor(),
                            white.get_truecolor(),
                            cross_fade=min((triggers.now - time) / fade_time, 1),
                        )
                    )
                )
            ),
        )
        for time in triggers.times
    ]

    fun = Align.center(
        Panel(
            Text("\n", justify="center").join(lines),
            border_style=Style(
                color=Color.from_triplet(
                    blend_rgb(
                        green.get_truecolor(),
                        red.get_truecolor(),
                        cross_fade=min(triggers.time_since_last_trigger / fade_time, 1),
                    )
                ),
            ),
            title="Trigger Tracker",
        )
    )
    return RenderGroup(info, fun, ball if len(triggers) > 2 else Text(""))


@DECK.slide(title="Views")
def grid():
    markup = dedent(
        """\
    ## Multiple Views

    Try pressing `d` to go into "deck" view.
    Press `s` to go back to "slide" view.

    Press `j`, then enter a slide number (like `3`) to jump to a slide.
    """
    )
    return Markdown(markup, justify="center")


@DECK.slide(title="Watch Mode")
def watch():
    markup = dedent(
        f"""\
    ## Developing a Deck

    {SPIEL} can reload your deck as you edit it if you add the `--watch` option to `present`:

    `$ spiel present path/to/deck.py --watch`

    If you're on a system without inotify support (e.g., Windows Subsystem for Linux), you may need to use the `--poll` option instead.

    When you're ready to present your deck for real, just drop the `--watch` option.
    """
    )
    return Markdown(markup, justify="center")


@DECK.slide(title="Displaying Images")
def image():
    markup = dedent(
        f"""\
    ## Images

    {SPIEL} can display images... sort of!

    If you see big chunks of constant color instead of smooth gradients, your terminal is probably not configured for "truecolor" mode.
    If your terminal supports truecolor (it probably does), try setting the environment variable `COLORTERM` to `truecolor`.
    For example, for `bash`, you could add

    `export COLORTERM=truecolor`

    to your `.bashrc` file, then restart your shell.
    """
    )
    root = Layout()
    root.split_row(
        Layout(Padding(Markdown(markup, justify="center"), pad=(0, 2))),
        Layout(Image.from_file(THIS_DIR / "img.jpg")),
    )

    return root
