from math import floor

from rich.align import Align
from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.text import Text

from spiel import Deck, Triggers

deck = Deck(name="Trigger Examples")


@deck.slide(title="Animating Content")
def animate(triggers: Triggers) -> RenderableType:
    bang = "!"
    space = "  "
    bar_length = 5

    spaces_before_face = min(floor(triggers.time_since_first_trigger), bar_length)
    spaces_after_face = bar_length - spaces_before_face

    bar = (space * spaces_before_face) + bang + (space * spaces_after_face)

    return Align(
        Group(
            Align.center(Text(f"{triggers.time_since_first_trigger=:.1f}")),
            Align.center(Text(f"{spaces_before_face=} | {spaces_after_face=}")),
            Align.center(Panel(Text(bar), expand=False, height=3)),
        ),
        align="center",
        vertical="middle",
    )
