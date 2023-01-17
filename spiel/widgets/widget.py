from __future__ import annotations

from typing import TYPE_CHECKING

from textual.reactive import watch
from textual.widget import Widget

from spiel.slide import Slide

if TYPE_CHECKING:
    from spiel.app import SpielApp


class SpielWidget(Widget):
    app: "SpielApp"

    def on_mount(self) -> None:
        watch(self.app, "deck", self.r)
        watch(self.app, "current_slide_idx", self.r)
        watch(self.app, "message", self.r)

    def r(self, _: object) -> None:
        self.refresh()

    @property
    def current_slide(self) -> Slide:
        return self.app.deck[self.app.current_slide_idx]
