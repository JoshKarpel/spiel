from __future__ import annotations

from typing import TYPE_CHECKING

from textual.reactive import _watch
from textual.widget import Widget

from spiel.slide import Slide

if TYPE_CHECKING:
    from spiel.app import SpielApp


class SpielWidget(Widget):
    app: "SpielApp"

    def on_mount(self) -> None:
        _watch(self, self.app, "deck", self.r)
        _watch(self, self.app, "current_slide_idx", self.r)
        _watch(self, self.app, "message", self.r)

    def r(self) -> None:
        self.refresh()

    @property
    def current_slide(self) -> Slide:
        return self.app.deck[self.app.current_slide_idx]
