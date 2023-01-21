from __future__ import annotations

from textual.app import ComposeResult
from textual.reactive import reactive

from spiel.constants import Direction, Transition
from spiel.screens.screen import SpielScreen
from spiel.slide import Slide
from spiel.triggers import Triggers
from spiel.widgets.fixed_slide import FixedSlideWidget
from spiel.widgets.footer import Footer


class SlideTransitionScreen(SpielScreen):
    DEFAULT_CSS = """\
    SlideTransitionScreen {
        layout: vertical;
        overflow: hidden hidden;
        layers: below above;
    }

    FixedSlideWidget#from {
        layer: above
    }

    FixedSlideWidget#to {
        layer: below
    }

    Footer {
        layer: above
    }
    """
    progress = reactive(0, init=False, layout=True)

    def __init__(
        self,
        from_slide: Slide,
        from_triggers: Triggers,
        to_slide: Slide,
        effect: Transition,
        direction: Direction,
    ):
        super().__init__()

        self.from_slide = from_slide
        self.from_triggers = from_triggers
        self.to_slide = to_slide
        self.effect = effect
        self.direction = direction

    def compose(self) -> ComposeResult:
        from_widget = FixedSlideWidget(self.from_slide, triggers=self.from_triggers, id="from")
        yield from_widget

        to_widget = FixedSlideWidget(self.to_slide, id="to")
        match self.effect, self.direction:
            case Transition.Swipe, Direction.Right:
                to_widget.styles.offset = ("100%", 0)
            case Transition.Swipe, Direction.Left:
                to_widget.styles.offset = ("-100%", 0)
        yield to_widget

        yield Footer()

    def watch_progress(self, new_progress: float) -> None:
        from_widget = self.query_one("#from")
        to_widget = self.query_one("#to")

        match self.effect, self.direction:
            case Transition.Swipe, Direction.Right:
                from_widget.styles.offset = (f"-{new_progress:.1f}%", 0)
                to_widget.styles.offset = (f"{100 - new_progress:.1f}%", 0)
            case Transition.Swipe, Direction.Left:
                from_widget.styles.offset = (f"{new_progress:.1f}%", 0)
                to_widget.styles.offset = (f"-{100 - new_progress:.1f}%", 0)
