from __future__ import annotations

from textual.app import ComposeResult
from textual.reactive import reactive

from spiel.screens.screen import SpielScreen
from spiel.slide import Slide
from spiel.widgets.footer import Footer
from spiel.widgets.slide import FixedSlideWidget


class SlideTransitionScreen(SpielScreen):
    DEFAULT_CSS = """\
    SlideTransitionScreen {
        layout: vertical;
        overflow: hidden hidden;
    }

    FixedSlideWidget#to {
        offset: 100% -100%;
    }
    """
    progress = reactive(0, init=False, layout=True)

    def __init__(self, from_slide: Slide, to_slide: Slide):
        super().__init__()

        self.from_slide = from_slide
        self.to_slide = to_slide

    def compose(self) -> ComposeResult:
        yield FixedSlideWidget(self.from_slide, id="from")
        yield FixedSlideWidget(self.to_slide, id="to")
        yield Footer()

    def watch_progress(self, new_progress: float) -> None:
        from_widget = self.query_one("#from")
        to_widget = self.query_one("#to")

        from_widget.styles.offset = (f"-{new_progress:.0f}%", 0)
        to_widget.styles.offset = (f"{100 - new_progress:.0f}%", "-100%")
