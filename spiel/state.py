from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from tempfile import TemporaryDirectory
from time import monotonic
from types import TracebackType
from typing import Callable, List, Optional, Type, Union

from rich.console import Console
from rich.style import Style
from rich.text import Text

from .constants import PACKAGE_NAME
from .deck import Deck
from .load import load_deck_and_options
from .modes import Mode
from .options import Options
from .presentable import Presentable

TextLike = Union[Text, Callable[[], Text]]


@dataclass
class State:
    console: Console
    deck: Deck
    options: Options
    _current_slide_idx: int = 0
    _mode: Mode = Mode.SLIDE
    _message: TextLike = Text("")
    trigger_times: List[float] = field(default_factory=list)

    @classmethod
    def from_file(cls, path: Path) -> State:
        deck, options = load_deck_and_options(path)
        return cls(console=Console(), deck=deck, options=options)

    @property
    def mode(self) -> Mode:
        return self._mode

    @mode.setter
    def mode(self, mode: Mode) -> None:
        self._mode = mode
        self.reset_trigger()

    @property
    def current_slide_idx(self) -> int:
        return self._current_slide_idx

    @current_slide_idx.setter
    def current_slide_idx(self, idx: int) -> None:
        self._current_slide_idx = max(0, min(len(self.deck) - 1, idx))
        self.reset_trigger()

    def next_slide(self, move: int = 1) -> None:
        if self.current_slide_idx == len(self.deck) - 1:
            return
        self.current_slide_idx += move

    def previous_slide(self, move: int = 1) -> None:
        if self.current_slide_idx == 0:
            return
        self.current_slide_idx -= move

    def jump_to_slide(self, idx: int) -> None:
        self.current_slide_idx = idx

    @property
    def current_slide(self) -> Presentable:
        return self.deck[self.current_slide_idx]

    @property
    def message(self) -> Text:
        if callable(self._message):
            try:
                return self._message()
            except Exception:
                return Text(
                    "Internal Error: failed to display message.",
                    style=Style(color="bright_red"),
                )
        else:
            return self._message

    def set_message(self, message: TextLike) -> None:
        self._message = message

    def clear_message(self) -> None:
        self.set_message(Text(""))

    @property
    def deck_grid_width(self) -> int:
        return max(self.console.size.width // 30, 1)

    def trigger(self) -> None:
        self.trigger_times.append(monotonic())

    def reset_trigger(self) -> None:
        self.trigger_times.clear()
        self.trigger()

    @cached_property
    def _tmp_dir(self) -> TemporaryDirectory:
        return TemporaryDirectory(prefix=f"{PACKAGE_NAME}-")

    @cached_property
    def tmp_dir(self) -> Path:
        return Path(self._tmp_dir.name)

    def __enter__(self) -> State:
        return self

    def __exit__(
        self,
        exctype: Optional[Type[BaseException]],
        excinst: Optional[BaseException],
        exctb: Optional[TracebackType],
    ) -> None:
        self._tmp_dir.cleanup()
