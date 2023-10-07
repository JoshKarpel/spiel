from __future__ import annotations

from typing import ClassVar, List

from textual.app import ComposeResult
from textual.binding import Binding

from spiel.screens.screen import SpielScreen
from spiel.widgets.footer import Footer
from spiel.widgets.minislides import MiniSlides


class DeckScreen(SpielScreen):
    BINDINGS: ClassVar[List[Binding]] = [
        Binding("right", "next_slide", "Go to next slide."),
        Binding("left", "prev_slide", "Go to previous slide."),
        Binding("down", "next_row", "Go to next row of slides."),
        Binding("up", "prev_row", "Go to previous row of slides."),
        Binding(
            "escape,enter", "switch_screen('slide')", "Go to Slide view with the selected slide."
        ),
    ]

    def compose(self) -> ComposeResult:
        yield MiniSlides()
        yield Footer()
