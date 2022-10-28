from __future__ import annotations

import datetime

from rich.console import Group, RenderableType
from rich.rule import Rule
from rich.style import Style
from rich.table import Column, Table
from rich.text import Text
from textual.widget import Widget


class Footer(Widget):
    DEFAULT_CSS = """
    Footer {
        color: $text;
        dock: bottom;
        height: 2;
    }
    """

    def on_mount(self) -> None:
        self.set_interval(1 / 60, self.refresh)

    @property
    def longest_slide_number_length(self) -> int:
        num_slides = len(self.app.deck)
        return len(str(num_slides))

    def render(self) -> RenderableType:
        grid = Table.grid(
            Column(
                style=Style(dim=True),
                justify="left",
            ),
            Column(
                style=Style(bold=True),
                justify="center",
            ),
            Column(
                style=Style(dim=True),
                justify="right",
            ),
            expand=True,
            padding=1,
        )
        grid.add_row(
            Text(
                f"{self.app.deck.name} | {self.app.current_slide.title} [{self.app.slide_idx + 1:>0{self.longest_slide_number_length}d} / {len(self.app.deck)}]"
            ),
            self.app.message,
            datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p"),
        )
        return Group(Rule(style=Style(dim=True)), grid)
