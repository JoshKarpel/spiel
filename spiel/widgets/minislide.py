from __future__ import annotations

from rich.console import RenderableType
from rich.panel import Panel
from rich.style import Style
from textual.widget import Widget


class MiniSlide(Widget):
    def __init__(self, slide_idx: int, **kwargs):
        super().__init__(**kwargs)

        self.slide_idx = slide_idx

    @property
    def is_active_slide(self) -> bool:
        return self.app.slide_idx == self.slide_idx

    def render(self) -> RenderableType:
        slide = self.app.deck[self.slide_idx]

        return Panel(
            renderable=slide.content(),
            title=f"[{self.slide_idx + 1}] {slide.title}",
            border_style=Style(
                color="bright_cyan" if self.is_active_slide else None,
                dim=not self.is_active_slide,
            ),
        )

    def on_mount(self) -> None:
        self.set_interval(1 / 10, self.refresh)