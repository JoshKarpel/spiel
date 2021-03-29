from dataclasses import dataclass
from datetime import date

from rich.console import ConsoleRenderable
from rich.style import Style
from rich.table import Column, Table

from orate.state import Stateful


@dataclass
class Footer(Stateful):
    @property
    def longest_slide_number_length(self) -> int:
        num_slides = len(self.state.deck)
        return len(str(num_slides))

    def __rich__(self) -> ConsoleRenderable:
        grid = Table.grid(
            Column(
                style=Style(dim=True),
                justify="left",
            ),
            Column(
                style=Style(dim=True),
                justify="center",
            ),
            Column(
                style=Style(dim=True),
                justify="right",
            ),
            expand=True,
        )
        grid.add_row(
            self.state.deck.name,
            date.today().isoformat(),
            f"[{self.state.current_slide_idx + 1:>0{self.longest_slide_number_length}d} / {len(self.state.deck)}]",
        )
        return grid
