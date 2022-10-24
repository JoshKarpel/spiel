from __future__ import annotations

import asyncio
import datetime
import importlib.util
import sys
from asyncio import wait
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.rule import Rule
from rich.style import Style
from rich.table import Column, Table
from rich.text import Text
from textual import log
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.reactive import reactive
from textual.screen import Screen
from textual.widget import Widget
from watchfiles import awatch

from spiel.constants import (
    DECK,
    PACKAGE_NAME,
    __python_version__,
    __rich_version__,
    __textual_version__,
    __version__,
)
from spiel.utils import clamp, drop_nones, filter_join


@dataclass
class Slide:
    title: str
    content: Callable[[], RenderableType]
    dynamic: bool


class SpielException(Exception):
    pass


class NoDeckFound(SpielException):
    pass


def load_deck(path: Path) -> Deck:
    module_name = "__deck"
    spec = importlib.util.spec_from_file_location(module_name, path)

    if spec is None:
        raise FileNotFoundError(
            f"{path.resolve()} does not appear to be an importable Python module."
        )

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module

    loader = spec.loader
    assert loader is not None
    loader.exec_module(module)

    try:
        deck = getattr(module, DECK)
    except AttributeError:
        raise NoDeckFound(f"The module at {path} does not have an attribute named {DECK}.")

    if not isinstance(deck, Deck):
        raise NoDeckFound(
            f"The module at {path} has an attribute named {DECK}, but it is a {type(deck).__name__}, not a {Deck.__name__}."
        )

    return deck


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
    def on_mount(self) -> None:
        self.set_interval(1 / 60, self.refresh)

    def render(self) -> RenderableType:
        slide = self.app.deck.slides[self.app.slide_idx]
        rendered_content = slide.content()
        return rendered_content


class MiniSlide(Widget):
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


class SlideScreen(Screen):
    DEFAULT_CSS = """
    SlideView {
        layout: vertical;
    }
    """

    def compose(self) -> ComposeResult:
        yield SlideWidget()
        yield Footer()


class DeckScreen(Screen):
    DEFAULT_CSS = """
    DeckView {
        layout: grid;
        grid-size: 4;
        grid-rows: 25%;
    }
    """

    BINDINGS = [
        ("escape,enter,down", "pop_screen", "Close"),
    ]

    def compose(self) -> ComposeResult:
        for idx, slide in enumerate(self.app.deck.slides):
            yield MiniSlide(slide=slide, slide_idx=idx)

        yield Footer()


class VersionDetails(Widget):
    DEFAULT_CSS = """
    VersionDetails {
        width: auto;
        height: auto;
    }
    """

    def render(self) -> RenderableType:
        console = self.app.console

        table = Table(
            Column(justify="right"),
            Column(justify="left"),
            show_header=False,
            box=None,
        )

        table.add_row(f"{PACKAGE_NAME.capitalize()} Version", __version__)
        table.add_row("Rich Version", __rich_version__)
        table.add_row("Textual Version", __textual_version__)
        table.add_row("Python Version", __python_version__)

        table.add_row(
            "Color System",
            Text(
                console.color_system or "unknown",
                style=Style(color="red" if console.color_system != "truecolor" else "green"),
            ),
        )
        table.add_row(
            "Console Dimensions",
            Text(f"{console.width} cells wide, {console.height} cells tall"),
            end_section=True,
        )

        return Panel(table)


class HelpScreen(Screen):
    DEFAULT_CSS = """
    Screen {
        align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield VersionDetails()
        yield Footer()


class Footer(Widget):
    DEFAULT_CSS = """
    Footer {
        color: $text;
        dock: bottom;
        height: 2;
    }
    """

    def on_mount(self) -> None:
        self.set_interval(1 / 60, self.refresh)

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


async def reload(deck_path: Path, watch_path: Path, app: SpielApp) -> None:
    log(f"Watching {watch_path} for changes to reload {deck_path} on {app}")
    async for _ in awatch(watch_path):
        app.deck = load_deck(deck_path)
        app.slide_idx = clamp(app.slide_idx, 0, len(app.deck))
        app.message = f"Reloaded deck at {datetime.datetime.now().strftime('%H:%M:%S')}"


class SpielApp(App):

    CSS_PATH = "spiel.css"
    BINDINGS = [
        Binding("ctrl+d", "toggle_dark", "Toggle dark mode"),
        Binding("right", "next_slide", "Next Slide"),
        Binding("left", "prev_slide", "Previous Slide"),
        Binding("up", "push_screen('deck')", "Deck View"),
        Binding("question_mark", "push_screen('help')", "Help"),
    ]
    SCREENS = {"deck": DeckScreen(), "help": HelpScreen()}

    slide_idx = reactive(0)
    message = reactive("")

    def __init__(self, path: Path, watch: Path, **kwargs):
        super().__init__(**kwargs)

        self.deck_path = path
        self.watch_path = watch

    def on_mount(self):
        self.deck = load_deck(self.deck_path)

        self.reloader = asyncio.create_task(
            reload(
                deck_path=self.deck_path,
                watch_path=self.watch_path,
                app=self,
            )
        )

        self.push_screen(SlideScreen())

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

    async def action_quit(self) -> None:
        self.reloader.cancel()
        await wait([self.reloader], timeout=1)

        await super().action_quit()
