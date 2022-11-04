from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen

from spiel.widgets.footer import Footer
from spiel.widgets.slide import SlideWidget


class SlideScreen(Screen):
    DEFAULT_CSS = """
    Screen {
        layout: vertical;
    }
    """

    BINDINGS = [
        Binding("t", "trigger", "Trigger"),
    ]

    def compose(self) -> ComposeResult:
        yield SlideWidget()
        yield Footer()
