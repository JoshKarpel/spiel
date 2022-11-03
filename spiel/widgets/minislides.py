from __future__ import annotations

from itertools import islice
from math import ceil

from rich.console import RenderableType
from rich.layout import Layout
from rich.panel import Panel
from rich.style import Style

from spiel.utils import clamp, filter_join
from spiel.widgets.widget import SpielWidget


class MiniSlides(SpielWidget):
    def render(self) -> RenderableType:
        self.log(self.app.deck)

        grid_width = max(self.app.console.size.width // 35, 1)
        row_of_current_slide = self.app.current_slide_idx // grid_width
        num_rows = ceil(len(self.app.deck) / grid_width)
        start_row = clamp(
            value=row_of_current_slide - (grid_width // 2),
            lower=0,
            upper=max(num_rows - grid_width, 0),
        )
        start_slide_idx = grid_width * start_row
        self.log(f"{row_of_current_slide=}")
        self.log(f"{num_rows=}")
        self.log(f"{start_row=}")
        self.log(f"{start_slide_idx=}")
        slides = islice(enumerate(self.app.deck.slides), start_slide_idx, None)

        rows = [Layout(name=str(r)) for r in range(grid_width)]
        cols = [[Layout(name=f"{r}-{c}") for c in range(grid_width)] for r, _ in enumerate(rows)]

        root = Layout()
        root.split_column(*rows)
        for row, layouts in zip(rows, cols):
            for layout in layouts:
                slide_idx, slide = next(slides, (None, None))
                if slide_idx is None or slide is None:
                    layout.update("")
                else:
                    is_active_slide = slide_idx == self.app.current_slide_idx
                    self.log(
                        f"{layout=} {slide_idx=} {slide=} {is_active_slide=} {self.app.current_slide_idx=}"
                    )
                    layout.update(
                        Panel(
                            slide.render(),
                            title=filter_join(" | ", [slide_idx + 1, slide.title]),
                            border_style=Style(
                                color="bright_cyan" if is_active_slide else None,
                                dim=not is_active_slide,
                            ),
                        )
                    )
            row.split_row(*layouts)

        return root