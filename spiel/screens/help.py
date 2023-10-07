from __future__ import annotations

from typing import ClassVar, List

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container

from spiel.screens.screen import SpielScreen
from spiel.widgets.bindings import AppBindingsTableWidget, ScreenBindingsTableWidget
from spiel.widgets.footer import Footer


class HelpScreen(SpielScreen):
    DEFAULT_CSS = """
    .h-section {
        layout: horizontal;
        height: auto;
        align: center top;
        content-align: center top;
    }
    """

    BINDINGS: ClassVar[List[Binding]] = [
        Binding("escape,enter", "pop_screen", "Return to the previous view."),
    ]

    def compose(self) -> ComposeResult:
        yield Container(
            AppBindingsTableWidget(),
            classes="h-section",
        )
        yield Container(
            ScreenBindingsTableWidget(id="slide"),
            ScreenBindingsTableWidget(id="deck"),
            classes="h-section",
        )
        yield Container(
            ScreenBindingsTableWidget(id="help"),
            classes="h-section",
        )
        yield Footer()
