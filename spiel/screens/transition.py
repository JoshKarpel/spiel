from __future__ import annotations

from enum import Enum

from textual.app import ComposeResult
from textual.reactive import reactive

from spiel.screens.screen import SpielScreen
from spiel.slide import Slide
from spiel.triggers import Triggers
from spiel.widgets.fixed_slide import FixedSlideWidget
from spiel.widgets.footer import Footer


class Direction(Enum):
    Right = "right"
    Left = "left"


class SlideTransitionScreen(SpielScreen):
    DEFAULT_CSS = """\
    SlideTransitionScreen {
        layout: vertical;
        overflow: hidden hidden;
    }
    """
    progress = reactive(0, init=False, layout=True)

    def __init__(
        self,
        from_slide: Slide,
        from_triggers: Triggers,
        to_slide: Slide,
        direction: Direction,
    ):
        super().__init__()

        self.from_slide = from_slide
        self.from_triggers = from_triggers
        self.to_slide = to_slide
        self.direction = direction

    def compose(self) -> ComposeResult:
        yield FixedSlideWidget(self.from_slide, triggers=self.from_triggers, id="from")

        to_widget = FixedSlideWidget(self.to_slide, id="to")
        match self.direction:
            case Direction.Right:
                to_widget.styles.offset = ("100%", "-100%")
            case Direction.Left:
                to_widget.styles.offset = ("-100%", "-100%")
        yield to_widget

        yield Footer()

    def watch_progress(self, new_progress: float) -> None:
        from_widget = self.query_one("#from")
        to_widget = self.query_one("#to")

        match self.direction:
            case Direction.Right:
                from_widget.styles.offset = (f"-{new_progress:.0f}%", 0)
                to_widget.styles.offset = (f"{100 - new_progress:.0f}%", "-100%")
            case Direction.Left:
                from_widget.styles.offset = (f"{new_progress:.0f}%", 0)
                to_widget.styles.offset = (f"-{100 - new_progress:.0f}%", "-100%")
