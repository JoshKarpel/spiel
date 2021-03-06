from dataclasses import dataclass

from pendulum import now
from rich.console import ConsoleRenderable
from rich.style import Style
from rich.table import Column, Table
from rich.text import Text

from spiel.modes import Mode
from spiel.rps import RPSCounter
from spiel.state import State
from spiel.utils import drop_nones, joinify


@dataclass
class Footer:
    state: State
    rps_counter: RPSCounter

    @property
    def longest_slide_number_length(self) -> int:
        num_slides = len(self.state.deck)
        return len(str(num_slides))

    def __rich__(self) -> ConsoleRenderable:
        grid = Table.grid(
            *drop_nones(
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
                )
                if self.state.profiling
                else None,
                Column(
                    style=Style(dim=True),
                    justify="right",
                ),
                Column(
                    style=Style(dim=True),
                    justify="right",
                ),
            ),
            expand=True,
            padding=1,
        )
        grid.add_row(
            *drop_nones(
                Text(
                    joinify(
                        " | ",
                        [
                            self.state.deck.name,
                            self.state.current_slide.title
                            if self.state.mode is Mode.SLIDE
                            else None,
                        ],
                    )
                ),
                self.state.message,
                Text(f"{self.rps_counter.renders_per_second() :.2f} RPS")
                if self.state.profiling
                else None,
                now().format("YYYY-MM-DD hh:mm A"),
                Text(
                    f"[{self.state.current_slide_idx + 1:>0{self.longest_slide_number_length}d} / {len(self.state.deck)}]"
                )
                if self.state.mode is not Mode.HELP
                else Text(Mode.HELP.value, style=Style(italic=True)),
            )
        )
        return grid
