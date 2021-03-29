from __future__ import annotations

import sys
import termios
from contextlib import contextmanager
from enum import Enum, unique
from itertools import product
from typing import (
    Callable,
    Dict,
    Iterator,
    MutableMapping,
    NoReturn,
    Optional,
    TextIO,
    Tuple,
    Union,
)

from .exceptions import DuplicateInputHandler
from .modes import Mode
from .state import State

IFLAG = 0
OFLAG = 1
CFLAG = 2
LFLAG = 3
ISPEED = 4
OSPEED = 5
CC = 6


@contextmanager
def no_echo() -> Iterator[None]:
    fd = sys.stdin.fileno()

    old = termios.tcgetattr(fd)

    mode = old.copy()
    mode[LFLAG] = mode[LFLAG] & ~(termios.ECHO | termios.ICANON)
    mode[CC][termios.VMIN] = 1
    mode[CC][termios.VTIME] = 0

    try:
        termios.tcsetattr(fd, termios.TCSADRAIN, mode)
        yield
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


@unique
class SpecialCharacters(Enum):
    Up = "up"
    Down = "down"
    Right = "right"
    Left = "left"
    CtrlUp = "ctrl-up"
    CtrlDown = "ctrl-down"
    CtrlRight = "ctrl-right"
    CtrlLeft = "ctrl-left"
    ShiftUp = "shift-up"
    ShiftDown = "shift-down"
    ShiftRight = "shift-right"
    ShiftLeft = "shift-left"
    CtrlShiftUp = "ctrl-shift-up"
    CtrlShiftDown = "ctrl-shift-down"
    CtrlShiftRight = "ctrl-shift-right"
    CtrlShiftLeft = "ctrl-shift-left"
    Backspace = "backspace"
    CtrlSpace = "ctrl-space"
    Enter = "enter"

    @classmethod
    def from_character(cls, character: str) -> SpecialCharacters:
        return SPECIAL_CHARACTERS[character]


SPECIAL_CHARACTERS = {
    "\x1b[A": SpecialCharacters.Up,
    "\x1b[B": SpecialCharacters.Down,
    "\x1b[C": SpecialCharacters.Right,
    "\x1b[D": SpecialCharacters.Left,
    "\x1b[1;5A": SpecialCharacters.CtrlUp,
    "\x1b[1;5B": SpecialCharacters.CtrlDown,
    "\x1b[1;5C": SpecialCharacters.CtrlRight,
    "\x1b[1;5D": SpecialCharacters.CtrlLeft,
    "\x1b[1;2A": SpecialCharacters.ShiftUp,
    "\x1b[1;2B": SpecialCharacters.ShiftDown,
    "\x1b[1;2C": SpecialCharacters.ShiftRight,
    "\x1b[1;2D": SpecialCharacters.ShiftLeft,
    "\x1b[1;6A": SpecialCharacters.CtrlShiftUp,
    "\x1b[1;6B": SpecialCharacters.CtrlShiftDown,
    "\x1b[1;6C": SpecialCharacters.CtrlShiftRight,
    "\x1b[1;6D": SpecialCharacters.CtrlShiftLeft,
    "\x7f": SpecialCharacters.Backspace,
    "\x00": SpecialCharacters.CtrlSpace,
    "\n": SpecialCharacters.Enter,
}

ARROWS = [
    SpecialCharacters.Up,
    SpecialCharacters.Down,
    SpecialCharacters.Right,
    SpecialCharacters.Left,
]


def get_character(stream: TextIO) -> Union[str, SpecialCharacters]:
    result = stream.read(1)

    if result[-1] == "\x1b":
        result += stream.read(2)

    if result[-1] == "1":
        result += stream.read(3)

    try:
        return SpecialCharacters.from_character(result)
    except KeyError:
        return result


Character = Union[str, SpecialCharacters]
InputHandler = Callable[[State], Optional[NoReturn]]
InputHandlerKey = Tuple[Character, Mode]
InputHandlerDecorator = Callable[[InputHandler], InputHandler]

INPUT_HANDLERS: MutableMapping[InputHandlerKey, InputHandler] = {}  # type: ignore


def handle_input(state: State, stream: TextIO) -> Optional[NoReturn]:
    character = get_character(stream)

    try:
        handler = INPUT_HANDLERS[(character, state.mode)]
    except KeyError:
        return None

    return handler(state)


def input(
    *characters: Character,
    modes: Optional[Iterator[Mode]] = None,
) -> InputHandlerDecorator:
    def decorator(func: InputHandler) -> InputHandler:
        for character, mode in product(characters, modes or list(Mode)):
            key: InputHandlerKey = (character, mode)
            if key in INPUT_HANDLERS:
                raise DuplicateInputHandler(
                    f"{character} is already registered as an input handler for mode {mode}"
                )
            INPUT_HANDLERS[key] = func
        return func

    return decorator


@input(SpecialCharacters.Right)
def next_slide(state: State) -> None:
    state.next_slide()


@input(SpecialCharacters.Left)
def previous_slide(state: State) -> None:
    state.previous_slide()
