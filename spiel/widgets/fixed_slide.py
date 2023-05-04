from __future__ import annotations

import sys

from rich.box import HEAVY
from rich.console import RenderableType
from rich.errors import NotRenderableError
from rich.panel import Panel
from rich.protocol import is_renderable
from rich.style import Style
from rich.traceback import Traceback

import spiel
from spiel.exceptions import SpielException
from spiel.slide import Slide
from spiel.triggers import Triggers
from spiel.widgets.widget import SpielWidget


class FixedSlideWidget(SpielWidget):
    def __init__(
        self, slide: Slide, triggers: Triggers | None = None, id: str | None = None
    ) -> None:
        super().__init__(id=id)

        self.slide = slide
        self.triggers = triggers or Triggers.new()

    def render(self) -> RenderableType:
        try:
            self.remove_class("error")
            r = self.slide.render(triggers=self.triggers)
            if is_renderable(r):
                return r
            else:
                raise NotRenderableError(f"object {r!r} is not renderable")
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
                title="Slide content failed to render",
                border_style=Style(bold=True, color="red1"),
                box=HEAVY,
            )
