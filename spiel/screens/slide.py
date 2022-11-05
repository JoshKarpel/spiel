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
        Binding("right", "next_slide", "Go to next slide."),
        Binding("left", "prev_slide", "Go to previous slide."),
        Binding("t", "trigger", "Trigger the current slide."),
    ]

    def compose(self) -> ComposeResult:
        yield SlideWidget()
        yield Footer()
