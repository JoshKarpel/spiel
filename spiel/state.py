from dataclasses import dataclass
from typing import Callable, Union

from rich.console import Console
from rich.text import Text

from .modes import Mode
from .slides import Deck, Slide

TextLike = Union[Text, Callable[[], Text]]


@dataclass
class State:
    console: Console
    deck: Deck
    _current_slide_idx: int = 0
    mode: Mode = Mode.SLIDE
    _message: TextLike = Text("")

    @property
    def current_slide_idx(self) -> int:
        return self._current_slide_idx

    @current_slide_idx.setter
    def current_slide_idx(self, idx: int) -> None:
        self._current_slide_idx = max(0, min(len(self.deck) - 1, idx))

    def next_slide(self, move: int = 1) -> None:
        self.current_slide_idx += move

    def previous_slide(self, move: int = 1) -> None:
        self.current_slide_idx -= move

    def jump_to_slide(self, idx: int) -> None:
        self.current_slide_idx = idx

    @property
    def current_slide(self) -> Slide:
        return self.deck[self.current_slide_idx]

    @property
    def message(self) -> Text:
        if callable(self._message):
            return self._message()
        else:
            return self._message

    def set_message(self, message: TextLike) -> None:
        self._message = message

    @property
    def deck_grid_width(self) -> int:
        return self.console.size.width // 30


@dataclass
class Stateful:
    state: State
