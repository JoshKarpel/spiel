from __future__ import annotations

from datetime import datetime

from rich.console import Group, RenderableType
from rich.rule import Rule
from rich.style import Style
from rich.table import Column, Table
from rich.text import Text
from textual.reactive import reactive

from spiel.constants import FOOTER_TIME_FORMAT
from spiel.widgets.widget import SpielWidget


class Footer(SpielWidget):
    DEFAULT_CSS = """
    Footer {
        color: $text;
        dock: bottom;
        height: 2;
    }
    """

    now: datetime = reactive(datetime.now)  # type: ignore[arg-type,assignment]

    def on_mount(self) -> None:
        super().on_mount()

        self.set_interval(1 / 60, self.update_now)

    def update_now(self) -> None:
        self.now = datetime.now()

    @property
    def longest_slide_number_length(self) -> int:
        num_slides = len(self.app.deck)
        return len(str(num_slides))

    def render(self) -> RenderableType:
        grid = Table.grid(
            Column(style=Style(dim=True), justify="left"),
            Column(style=Style(bold=True), justify="center"),
            Column(style=Style(dim=True), justify="right"),
            expand=True,
            padding=1,
        )
        grid.add_row(
            Text(f"{self.app.deck.name} | {self.app.deck[self.app.current_slide_idx].title}"),
            self.app.message,
            Text(
                f"{self.now.strftime(FOOTER_TIME_FORMAT)}   [{self.app.current_slide_idx + 1:>0{self.longest_slide_number_length}d} / {len(self.app.deck)}]"
            ),
        )
        return Group(Rule(style=Style(dim=True)), grid)
