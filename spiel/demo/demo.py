#!/usr/bin/env python

import inspect
import shutil
import socket
from datetime import datetime
from math import cos, floor, pi
from pathlib import Path
from textwrap import dedent

from click import edit
from rich.align import Align
from rich.box import HEAVY, SQUARE
from rich.color import Color, blend_rgb
from rich.console import Group, RenderableType
from rich.layout import Layout
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.style import Style
from rich.syntax import Syntax
from rich.text import Text

from spiel import Slide, SuspendType, Triggers, present
from spiel.deck import Deck
from spiel.renderables.image import Image

deck = Deck(name=f"Spiel Demo Deck")

SPIEL = "[Spiel](https://github.com/JoshKarpel/spiel)"
RICH = "[Rich](https://rich.readthedocs.io/)"
IPYTHON = "[IPython](https://ipython.readthedocs.io)"
WSL = "[Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/)"

THIS_DIR = Path(__file__).resolve().parent


def pad_markdown(markup: str) -> RenderableType:
    return Padding(Markdown(dedent(markup), justify="center"), pad=(0, 5))


@deck.slide(title="What is Spiel?")
def what() -> RenderableType:
    upper_left = pad_markdown(
        f"""\
        ## What is Spiel?

        {SPIEL} is a framework for building and presenting richly-styled presentations in your terminal using Python.

        Spiel uses {RICH} to render slide content.
        Anything you can display with Rich, you can display with Spiel (plus some other things)!

        Use your right `→` and left `←` arrows keys to go forwards and backwards through the deck.

        Press `ctrl-c` to exit.

        Press `?` at any time to see the help screen, which describes all of the actions you can take.

        To get a copy of the source code for this deck, use the `spiel demo copy` command.
        """
    )

    upper_right = pad_markdown(
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

    lower_left = pad_markdown(
        f"""\
        ## Contributing

        Please report bugs via [GitHub Issues](https://github.com/JoshKarpel/spiel/issues).

        If you have ideas about how Spiel can be improved,
        or you have a cool deck to show off,
        please post to [GitHub Discussions](https://github.com/JoshKarpel/spiel/discussions).
        """
    )

    lower_right = pad_markdown(
        f"""\
        ## Inspirations

        Brandon Rhodes' [PyCon 2017](https://youtu.be/66P5FMkWoVU) and [North Bay Python 2017](https://youtu.be/rrMnmLyYjU8) talks.

        David Beazley's [Lambda Calculus from the Ground Up](https://youtu.be/pkCLMl0e_0k) tutorial at PyCon 2019.

        LaTeX's [Beamer](https://ctan.org/pkg/beamer) document class.
        """
    )

    root = Layout()
    upper = Layout()
    lower = Layout()

    upper.split_row(
        Layout(upper_left),
        Layout(upper_right),
    )
    lower.split_row(
        Layout(lower_left),
        Layout(lower_right),
    )
    root.split_column(upper, lower)

    return root


@deck.slide(title="Decks and Slides")
def code() -> RenderableType:
    markup = f"""\
        ## Decks are made of Slides

        Here's the code for `Deck` and `Slide`!

        The source code is pulled directly from the definitions via [inspect.getsource](https://docs.python.org/3/library/inspect.html#inspect.getsource).

        ({RICH} supports syntax highlighting, so {SPIEL} does too!)
        """
    root = Layout()
    upper = Layout(pad_markdown(markup), size=len(markup.split("\n")) + 1)
    lower = Layout()
    root.split_column(upper, lower)

    def make_code_panel(obj: type) -> RenderableType:
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


@deck.slide(title="Dynamic Content")
def dynamic() -> RenderableType:
    width = shutil.get_terminal_size().columns
    width_limit = 80

    home = Path.home()
    home_dir_contents = list(home.iterdir())

    return Group(
        Align.center(
            pad_markdown(
                f"""\
                ## Slides can have dynamic content!

                Since slides are created using normal Python code,
                any output you can imagine producing via Python can make it into your slides.

                Here are some examples:
                """
            ),
        ),
        Align.center(
            Panel(
                Text(
                    f"Your terminal is {width} cells wide (try resizing it or adjusting your font size!)"
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
                    f"The local timezone on this computer ([bold]{socket.gethostname()}[/bold]) is [bold]{datetime.now().astimezone().tzinfo}[/bold]",
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


@deck.slide(title="Triggers")
def triggers(triggers: Triggers) -> RenderableType:
    info = pad_markdown(
        f"""\
        ## Triggers

        Triggers are a mechanism for making dynamic content that depends on *relative* time.

        Triggers can be used to implement effects like fades, motion, and other "animations".

        Each slide is triggered once when it starts being displayed.

        You can trigger it again (as many times as you'd like) by pressing `t`.
        You can reset the trigger state by pressing `r`.

        This slide has been triggered {len(triggers)} times.

        It was last triggered {triggers.time_since_last_trigger:.2f} seconds ago.
        """
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
            f"Triggered at {time - triggers[0]:.3f}!",
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
        for time in triggers
    ]

    fun = Padding(
        Align.center(
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
        ),
        pad=(1, 0),
    )

    return Group(info, fun, ball if len(triggers) > 2 else Text(""))


@deck.slide(title="Views")
def grid() -> RenderableType:
    return pad_markdown(
        """\
        ## Deck View

        Try pressing `d` to go into "deck" view.
        You can move between slides in deck view using your arrow keys (right `→`, left `←`, up `↑`, and down `↓`).

        Press `enter` or `escape` to go back to "slide" view (this view),
        on the currently-selected slide.
        """
    )


@deck.slide(title="Displaying Images")
def image() -> RenderableType:
    markup = f"""\
        ## Images

        {SPIEL} can display images... sort of!

        Spiel includes an `Image` widget that can render images by interpolating pixel values.

        If you see big chunks of constant color instead of smooth gradients, your terminal is probably not configured for "truecolor" mode.
        If your terminal supports truecolor (it probably does), try setting the environment variable `COLORTERM` to `truecolor`.

        For example, for `bash`, you could add

        `export COLORTERM=truecolor`

        to your `.bashrc` file, then restart your shell.
        """

    image_path = THIS_DIR / "tree.jpg"
    root = Layout()
    root.split_row(
        Layout(pad_markdown(markup)),
        Layout(
            Panel.fit(
                Image.from_file(image_path),
                subtitle=str(image_path),
                box=HEAVY,
                padding=0,
            )
        ),
    )

    return root


@deck.slide(title="Watch Mode")
def watch() -> RenderableType:
    return pad_markdown(
        f"""\
        ## Developing a Deck

        {SPIEL} will reload your deck as you edit it to make development easier.

        The reload is triggered whenever any files under the path passed to the
        `--watch` argument of `spiel present` changes.
        That path defaults to your current working directory
        (right now it is `{Path.cwd()}`).
        """
    )


def edit_this_file(suspend: SuspendType) -> None:
    with suspend():
        edit(filename=__file__)


@deck.slide(
    title="Bindings",
    bindings={
        "e": edit_this_file,
    },
)
def bindings() -> RenderableType:
    edit_function_src = dedent("".join(inspect.getsourcelines(edit_this_file)[0]))
    return pad_markdown(
        f"""\
        ## Custom Per-Slide Key Bindings

        Custom keybindings can be added on a per-slide basis using the `bindings` argument of `@slide`,
        which takes a mapping of key names to callables to call when that key is pressed.

        ```python
        def edit_this_file(suspend: SuspendType) -> None:
            with suspend():
                edit(filename=__file__)

        @deck.slide(
            title="Bindings",
            bindings={{
                "e": edit_this_file,
            }},
        )
        def bindings() -> RenderableType:
            ...
        ```

        If the callable takes an argument named `suspend`,
        it will be passed a function that, when used as a context manager,
        suspends {SPIEL} while inside the `with` block.

        A binding has been registered on this slide that suspends {SPIEL}
        and opens your `$EDITOR` on this file.
        Try pressing `e`!

        Due to reloading, any changes you make will be reflected in the
        presentation you're seeing right now.
        """
    )


class DemoRenderFailure(Exception):
    pass


@deck.slide(title="Render Failure")
def failure() -> RenderableType:
    raise DemoRenderFailure(
        f"""Woops!

        An exception was raised while rendering this slide.

        When this happens, Spiel will display the stack trace to help you debug the problem.

        Deck reloading will still happen, so you can fix the error without stopping Spiel.
        """
    )


if __name__ == "__main__":
    present(__file__)
