from __future__ import annotations

from time import monotonic

from rich.console import RenderableType
from textual.reactive import reactive

from spiel.triggers import Triggers
from spiel.widgets.widget import SpielWidget


class SlideWidget(SpielWidget):
    triggers = reactive(Triggers._new)

    def on_mount(self) -> None:
        super().on_mount()

        self.set_interval(1 / 60, self.update_triggers)

    def update_triggers(self) -> None:
        self.triggers = Triggers(now=monotonic(), times=self.triggers.times)

    def render(self) -> RenderableType:
        return self.app.deck.slides[self.app.current_slide_idx].render(triggers=self.triggers)
