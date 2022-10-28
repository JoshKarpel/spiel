from __future__ import annotations

from rich.console import RenderableType
from textual.widget import Widget


class SlideWidget(Widget):
    def on_mount(self) -> None:
        self.set_interval(1 / 60, self.refresh)

    def render(self) -> RenderableType:
        slide = self.app.deck.slides[self.app.slide_idx]
        rendered_content = slide.content()
        return rendered_content
