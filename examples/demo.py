import socket
from datetime import datetime

from rich.align import Align
from rich.layout import Layout
from rich.markdown import Markdown
from rich.style import Style
from rich.text import Text

from spiel.slides import Deck, Slide

DECK = Deck(name="Spiel Demo Deck")

left_markup = """\
## What is Spiel?

[Spiel](https://github.com/JoshKarpel/spiel) is a framework for building slide decks in Python.

Orate uses [Rich](https://rich.readthedocs.io/) to render slide content.
"""

right_markup = """\
## Why Spiel?

It's fun!

It's weird!
"""

layout = Layout()
left = Layout(
    Markdown(
        left_markup,
        justify="center",
    ),
    ratio=2,
)
buffer = Layout(" ")
right = Layout(
    Markdown(
        right_markup,
        justify="center",
    ),
    ratio=2,
)
layout.split_row(left, buffer, right)

DECK.add_slide(
    Slide(
        content=layout,
    )
)


class Now:
    def __rich__(self):
        return Align(
            Text(
                f"Right now, at {datetime.now()}!",
                style=Style(color="bright_cyan", bold=True, italic=True),
            ),
            align="center",
        )


DECK.add_slide(
    Slide(
        content=Now(),
    )
)


class Where:
    def __rich__(self):
        return Align(
            Text(
                f"Right here, at {socket.gethostname()}!",
                style=Style(color="bright_cyan", bold=True, italic=True),
            ),
            align="right",
        )


DECK.add_slide(
    Slide(
        content=Where(),
    )
)
