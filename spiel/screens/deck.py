from __future__ import annotations

from textual.app import ComposeResult
from textual.screen import Screen

from spiel.widgets.footer import Footer
from spiel.widgets.minislides import MiniSlides


class DeckScreen(Screen):
    DEFAULT_CSS = """
    """

    BINDINGS = [
        ("escape,enter,down", "switch_screen('slide')", "Close"),
    ]

    def compose(self) -> ComposeResult:
        yield MiniSlides()
        yield Footer()
