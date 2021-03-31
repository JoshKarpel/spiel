from dataclasses import dataclass

from pendulum import now
from rich.console import ConsoleRenderable
from rich.style import Style
from rich.table import Column, Table

from spiel.modes import Mode
from spiel.state import Stateful
from spiel.utils import joinify


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
                style=Style(bold=True),
                justify="center",
            ),
            Column(
                style=Style(dim=True),
                justify="right",
            ),
            Column(
                style=Style(dim=True),
                justify="right",
            ),
            expand=True,
        )
        grid.add_row(
            joinify(
                " | ",
                [
                    self.state.deck.name,
                    self.state.current_slide.title if self.state.mode is Mode.SLIDE else None,
                ],
            ),
            self.state.message,
            now().format("YYYY-MM-DD hh:mm A"),
            f"[{self.state.current_slide_idx + 1:>0{self.longest_slide_number_length}d} / {len(self.state.deck)}]",
        )
        return grid
