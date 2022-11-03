from __future__ import annotations

from rich.console import RenderableType
from textual.reactive import watch
from textual.widget import Widget


class SlideWidget(Widget):
    def on_mount(self) -> None:
        self.set_interval(1 / 60, self.refresh)

        watch(self.app, "deck", self.r)
        watch(self.app, "current_slide_idx", self.r)

    def r(self, _):
        self.refresh()

    def render(self) -> RenderableType:
        return self.app.deck.slides[self.app.current_slide_idx].content()
