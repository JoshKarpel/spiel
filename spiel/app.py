from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Callable

from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.rule import Rule
from rich.style import Style
from rich.table import Column, Table
from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.reactive import reactive
from textual.screen import Screen
from textual.widget import Widget

from spiel.utils import clamp, drop_nones, filter_join


@dataclass
class Slide:
    title: str
    content: Callable[[], RenderableType]
    dynamic: bool


@dataclass
class Deck:
    name: str
    slides: list[slide] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.slides)

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


class SlideView(Screen):
    def compose(self) -> ComposeResult:
        yield SlideWidget()
        yield Footer()


class DeckView(Screen):
    BINDINGS = [
        ("escape,enter,down", "pop_screen", "Close"),
    ]

    def compose(self) -> ComposeResult:
        for idx, slide in enumerate(self.app.deck.slides):
            yield DeckViewSlideWidget(slide=slide, slide_idx=idx)

        yield Footer()


class Footer(Widget):
    DEFAULT_CSS = """
    Footer {
        color: $text;
        dock: bottom;
        height: 2;
    }
    """

    @property
    def longest_slide_number_length(self) -> int:
        num_slides = len(self.app.deck)
        return len(str(num_slides))

    def render(self) -> RenderableType:
        grid = Table.grid(
            *drop_nones(
                Column(
                    style=Style(dim=True),
                    justify="left",
                ),
                Column(
                    style=Style(bold=True),
                    justify="center",
                ),
                Column(
                    style=Style(dim=True),
                    justify="right",
                ),
                Column(
                    style=Style(dim=True),
                    justify="right",
                ),
            ),
            expand=True,
            padding=1,
        )
        grid.add_row(
            *drop_nones(
                Text(
                    filter_join(
                        " | ",
                        [self.app.deck.name, self.app.current_slide.title],
                    )
                ),
                self.app.message,
                datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p"),
                Text(
                    f"[{self.app.slide_idx + 1:>0{self.longest_slide_number_length}d} / {len(self.app.deck)}]"
                ),
            )
        )
        return Group(Rule(style=Style(dim=True)), grid)


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
    message = reactive("")

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Footer()

    def on_mount(self):
        from demo.demo import deck

        self.deck = deck

        self.push_screen(SlideView())

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_next_slide(self) -> None:
        self.slide_idx = clamp(self.slide_idx + 1, 0, len(self.deck) - 1)

    def action_prev_slide(self) -> None:
        self.slide_idx = clamp(self.slide_idx - 1, 0, len(self.deck) - 1)

    @property
    def current_slide(self) -> Slide:
        return self.deck.slides[self.slide_idx]


if __name__ == "__main__":
    app = SpielApp()
    app.run()
