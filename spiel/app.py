from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from rich.console import RenderableType
from rich.panel import Panel
from rich.style import Style
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.reactive import reactive
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Footer, Header


@dataclass
class Slide:
    title: str
    content: Callable[[], RenderableType]
    dynamic: bool


@dataclass
class Deck:
    name: str
    slides: list[slide] = field(default_factory=list)

    def slide(
        self,
        title: str = "",
        dynamic: bool = False,
    ):
        def slideify(content: Callable[[], RenderableType]) -> Slide:
            slide = Slide(title=title, content=content, dynamic=dynamic)
            self.slides.append(slide)
            return slide

        return slideify


class SlideWidget(Widget):
    can_focus = True
    can_focus_children = True

    def on_mount(self) -> None:
        self.set_interval(1 / 60, self.refresh)

    def render(self) -> RenderableType:
        slide = self.app.deck.slides[self.app.slide_idx]
        rendered_content = slide.content()
        return rendered_content


class DeckViewSlideWidget(Widget):
    def __init__(self, slide, slide_idx, **kwargs):
        super().__init__(**kwargs)
        self.slide = slide
        self.slide_idx = slide_idx

    @property
    def is_active_slide(self) -> bool:
        return self.app.slide_idx == self.slide_idx

    def render(self) -> RenderableType:
        return Panel(
            self.slide.content(),
            title=self.slide.title,
            border_style=Style(
                color="bright_cyan" if self.is_active_slide else None,
                dim=not self.is_active_slide,
            ),
        )

    def on_mount(self) -> None:
        self.set_interval(1 / 10, self.refresh)


class DeckView(Screen):
    #: Bindings for the help screen.
    BINDINGS = [
        ("escape,enter,down", "pop_screen", "Close"),
    ]

    def compose(self) -> ComposeResult:
        for idx, slide in enumerate(self.app.deck.slides):
            yield DeckViewSlideWidget(slide=slide, slide_idx=idx)


class SpielApp(App):

    CSS_PATH = "spiel.css"
    BINDINGS = [
        Binding("d", "toggle_dark", "Toggle dark mode"),
        Binding("right", "next_slide", "Next Slide"),
        Binding("left", "prev_slide", "Previous Slide"),
        Binding("up", "push_screen('deck')", "Deck View"),
    ]
    SCREENS = {"deck": DeckView()}

    slide_idx = reactive(0)

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield SlideWidget()

    def on_mount(self):
        from demo.demo import deck

        self.deck = deck

        w = self.query_one(SlideWidget)
        w.slide_idx = 0

        self.log(w)
        w.focus()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_next_slide(self) -> None:
        if self.slide_idx < len(self.deck.slides) - 1:
            self.slide_idx += 1

    def action_prev_slide(self) -> None:
        if self.slide_idx > 0:
            self.slide_idx -= 1


if __name__ == "__main__":
    app = SpielApp()
    app.run()
