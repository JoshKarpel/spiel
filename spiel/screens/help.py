from __future__ import annotations

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static

from spiel.renderables.version import DebugTable
from spiel.widgets.footer import Footer


class HelpScreen(Screen):
    DEFAULT_CSS = """
    Screen {
        align: center middle;
    }

    .content-center {
        content-align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static(DebugTable(), classes="content-center")
        yield Footer()
