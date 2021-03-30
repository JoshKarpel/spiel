import string
from random import sample

from rich.text import Text

from spiel import Deck, Slide

DECK = Deck(
    name="Many Slides",
    slides=[
        Slide(Text(f"This is slide {n + 1}"), title="".join(sample(string.ascii_letters, 30)))
        for n in range(30)
    ],
)
