from dataclasses import dataclass

from .modes import Mode
from .slides import Deck, Slide


@dataclass
class State:
    deck: Deck
    _current_slide_idx: int = 0
    mode: Mode = Mode.SLIDE

    @property
    def current_slide_idx(self) -> int:
        return self._current_slide_idx

    @current_slide_idx.setter
    def current_slide_idx(self, idx: int) -> None:
        self._current_slide_idx = max(0, min(len(self.deck) - 1, idx))

    def next_slide(self, n: int = 1) -> None:
        self.current_slide_idx += n

    def previous_slide(self, n: int = 1) -> None:
        self.current_slide_idx -= n

    @property
    def current_slide(self) -> Slide:
        return self.deck[self.current_slide_idx]


@dataclass
class Stateful:
    state: State
