from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from rich.console import RenderableType
from rich.repr import Result
from textual.app import App, ComposeResult
from textual.reactive import reactive
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

    slide_idx = reactive(0)
    d = reactive(False)

    def __init__(
        self,
        deck: Deck,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        super().__init__(name=name, id=id, classes=classes)

        self.deck = deck

    def on_mount(self) -> None:
        self.set_interval(1 / 60, self.refresh)

    def render(self) -> RenderableType:
        slide = self.deck.slides[self.slide_idx]
        rendered_content = slide.content()
        return rendered_content

    def __rich_repr__(self) -> Result:
        yield "deck", self.deck
        yield "slide_idx", self.slide_idx


class SpielApp(App):

    CSS_PATH = "spiel.css"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("right", "next_slide", "Next Slide"),
        ("left", "prev_slide", "Previous Slide"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield SlideWidget(deck=Deck(name="New Deck"))

    def on_mount(self):
        from demo.demo import deck

        w = self.query_one(SlideWidget)
        w.deck = deck
        w.slide_idx = 0

        self.log(w)
        w.focus()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_next_slide(self) -> None:
        w = self.query_one(SlideWidget)
        if w.slide_idx < len(w.deck.slides) - 1:
            w.slide_idx += 1

    def action_prev_slide(self) -> None:
        w = self.query_one(SlideWidget)
        if w.slide_idx >= 0:
            w.slide_idx -= 1


if __name__ == "__main__":
    app = SpielApp()
    app.run()
