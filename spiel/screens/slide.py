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
        Binding("r", "reset_trigger", "Reset trigger state."),
        Binding("e", "edit", "Edit the current slide's edit target."),
    ]

    def compose(self) -> ComposeResult:
        yield SlideWidget()
        yield Footer()
