from __future__ import annotations

import inspect
from typing import ClassVar, List, Tuple

from textual.app import ComposeResult
from textual.binding import Binding
from textual.events import Key

from spiel.screens.screen import SpielScreen
from spiel.widgets.footer import Footer
from spiel.widgets.slide import SlideWidget

SUSPEND = "suspend"


class SlideScreen(SpielScreen):
    BINDINGS: ClassVar[List[Binding | Tuple[str, str, str]]] = [
        Binding("right", "next_slide", "Go to next slide."),
        Binding("left", "prev_slide", "Go to previous slide."),
        Binding("t", "trigger", "Trigger the current slide."),
        Binding("r", "reset_trigger", "Reset trigger state."),
    ]

    def compose(self) -> ComposeResult:
        yield SlideWidget()
        yield Footer()

    def on_key(self, event: Key) -> None:
        slide = self.app.deck[self.app.current_slide_idx]
        bind = slide.bindings.get(event.key)

        if callable(bind):
            signature = inspect.signature(bind)

            kwargs: dict[str, object] = {}
            if SUSPEND in signature.parameters:
                kwargs[SUSPEND] = self.app.suspend

            bind(**kwargs)
