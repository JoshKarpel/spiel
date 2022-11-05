from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen

from spiel.widgets.footer import Footer
from spiel.widgets.minislides import MiniSlides


class DeckScreen(Screen):
    DEFAULT_CSS = """
    """

    BINDINGS = [
        Binding("right", "next_slide", "Next Slide"),
        Binding("left", "prev_slide", "Previous Slide"),
        Binding("up", "prev_row", "Previous Row"),
        Binding("down", "next_row", "Next Row"),
        Binding("escape,enter", "switch_screen('slide')", "Close"),
    ]

    def compose(self) -> ComposeResult:
        yield MiniSlides()
        yield Footer()
