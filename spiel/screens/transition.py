from __future__ import annotations

from typing import Type

from textual.app import ComposeResult
from textual.reactive import reactive

from spiel.screens.screen import SpielScreen
from spiel.slide import Slide
from spiel.transitions.protocol import Direction, Transition
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
        layer: above;
    }

    FixedSlideWidget#to {
        layer: below;
    }

    Footer {
        layer: above;
    }

    Footer#dummy {
        layer: below;
    }
    """
    progress = reactive(0, init=False, layout=True)

    def __init__(
        self,
        from_slide: Slide,
        from_triggers: Triggers,
        to_slide: Slide,
        transition: Type[Transition],
        direction: Direction,
    ) -> None:
        super().__init__()

        self.from_slide = from_slide
        self.from_triggers = from_triggers
        self.to_slide = to_slide
        self.transition = transition()
        self.direction = direction

    def compose(self) -> ComposeResult:
        from_widget = FixedSlideWidget(self.from_slide, triggers=self.from_triggers, id="from")
        to_widget = FixedSlideWidget(self.to_slide, id="to")

        self.transition.initialize(
            from_widget=from_widget,
            to_widget=to_widget,
            direction=self.direction,
        )

        yield from_widget
        yield to_widget

        yield Footer()
        yield Footer(
            id="dummy"
        )  # a dummy footer to hold space on the "below" layer, won't be displayed

    def watch_progress(self, new_progress: float) -> None:
        from_widget = self.query_one("#from")
        to_widget = self.query_one("#to")

        self.transition.progress(
            from_widget=from_widget,
            to_widget=to_widget,
            direction=self.direction,
            progress=new_progress,
        )
