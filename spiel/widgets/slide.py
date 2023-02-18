from __future__ import annotations

import sys
from time import monotonic

from rich.box import HEAVY
from rich.console import RenderableType
from rich.errors import NotRenderableError
from rich.panel import Panel
from rich.protocol import is_renderable
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

        self.set_interval(self.app.slide_refresh_rate, self.update_triggers)

    def update_triggers(self) -> None:
        self.triggers = Triggers(now=monotonic(), _times=self.triggers._times)

    def render(self) -> RenderableType:
        try:
            self.remove_class("error")
            r = self.current_slide.render(triggers=self.triggers)
            if is_renderable(r):
                return r
            else:
                raise NotRenderableError(f"object {r!r} is not renderable")
        except Exception:
            self.add_class("error")
            et, ev, tr = sys.exc_info()
            if et is None or ev is None or tr is None:  # pragma: unreachable
                raise SpielException("Expected to be handling an exception, but wasn't.")
            return Panel(
                Traceback.from_exception(
                    exc_type=et,
                    exc_value=ev,
                    traceback=tr,
                    suppress=(spiel,),
                ),
                title="Slide content failed to render",
                border_style=Style(bold=True, color="red1"),
                box=HEAVY,
            )
