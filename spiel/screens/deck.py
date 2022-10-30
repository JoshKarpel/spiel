from __future__ import annotations

from textual.app import ComposeResult
from textual.screen import Screen

from spiel.widgets.footer import Footer
from spiel.widgets.minislide import MiniSlide


class DeckScreen(Screen):
    DEFAULT_CSS = """
    Screen {
        layout: grid;
        grid-size: 4;
        grid-rows: 25%;
    }
    """

    BINDINGS = [
        ("escape,enter,down", "pop_screen", "Close"),
    ]

    def compose(self) -> ComposeResult:
        for idx, slide in enumerate(self.app.deck.slides):
            yield MiniSlide(slide_idx=idx)

        yield Footer()
