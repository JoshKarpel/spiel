from __future__ import annotations

import sys
from time import monotonic

from rich.box import HEAVY
from rich.console import RenderableType
from rich.padding import Padding
from rich.panel import Panel
from rich.style import Style
from rich.traceback import Traceback
from textual.reactive import reactive

import spiel
from spiel.exceptions import SpielException
from spiel.triggers import Triggers
from spiel.widgets.widget import SpielWidget


class SlideWidget(SpielWidget):
    triggers: Triggers = reactive(Triggers.new)  # type: ignore[assignment,arg-type]

    def on_mount(self) -> None:
        super().on_mount()

        self.set_interval(1 / 60, self.update_triggers)

    def update_triggers(self) -> None:
        self.triggers = Triggers(now=monotonic(), times=self.triggers.times)

    def render(self) -> RenderableType:
        try:
            self.remove_class("error")
            slide = self.app.deck[self.app.current_slide_idx]
            return Padding(slide.render(triggers=self.triggers), pad=slide.pad)
        except Exception:
            self.add_class("error")
            et, ev, tr = sys.exc_info()
            if et is None or ev is None or tr is None:
                raise SpielException("Expected to be handling an exception, but wasn't.")
            return Panel(
                Traceback.from_exception(
                    exc_type=et,
                    exc_value=ev,
                    traceback=tr,
                    suppress=(spiel,),
                ),
                title="Slide failed to render",
                border_style=Style(bold=True, color="red1"),
                box=HEAVY,
            )
