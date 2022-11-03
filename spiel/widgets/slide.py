from __future__ import annotations

from rich.console import RenderableType

from spiel.widgets.widget import SpielWidget


class SlideWidget(SpielWidget):
    def on_mount(self) -> None:
        super().on_mount()

        self.set_interval(1 / 60, self.refresh)

    def render(self) -> RenderableType:
        return self.app.deck.slides[self.app.current_slide_idx].content()
