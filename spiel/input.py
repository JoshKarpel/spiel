from __future__ import annotations

import string
import sys
import termios
from contextlib import contextmanager
from enum import Enum, unique
from io import UnsupportedOperation
from itertools import product
from typing import (
    Callable,
    Iterable,
    Iterator,
    MutableMapping,
    NoReturn,
    Optional,
    TextIO,
    Tuple,
    Union,
)

from rich.text import Text
from typer import Exit

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
    try:
        fd = sys.stdin.fileno()
    except UnsupportedOperation:
        yield
        return

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
    CtrlK = "ctrl-k"
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
    "\x0b": SpecialCharacters.CtrlK,
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

    if result == "":  # this happens when stdin gets closed; equivalent to a quit
        raise Exit(code=0)

    if result[-1] == "\x1b":
        result += stream.read(2)

    if len(result) != 1 and result[-1] == "1":
        result += stream.read(3)

    try:
        return SpecialCharacters.from_character(result)
    except KeyError:
        return result


Character = Union[str, SpecialCharacters]
InputHandler = Callable[[State], Optional[NoReturn]]
InputHandlerKey = Tuple[Character, Mode]
InputHandlerDecorator = Callable[[InputHandler], InputHandler]
InputHandlers = MutableMapping[InputHandlerKey, InputHandler]

INPUT_HANDLERS: InputHandlers = {}  # type: ignore


def handle_input(state: State, stream: TextIO) -> Optional[NoReturn]:
    character = get_character(stream)

    try:
        handler = INPUT_HANDLERS[(character, state.mode)]
    except KeyError:
        return None

    return handler(state)


def input_handler(
    *characters: Character,
    modes: Optional[Iterable[Mode]] = None,
    handlers: InputHandlers = INPUT_HANDLERS,
) -> InputHandlerDecorator:
    def decorator(func: InputHandler) -> InputHandler:
        for character, mode in product(characters, modes or list(Mode)):
            key: InputHandlerKey = (character, mode)
            if key in handlers:
                raise DuplicateInputHandler(
                    f"{character} is already registered as an input handler for mode {mode}"
                )
            handlers[key] = func
        return func

    return decorator


@input_handler(SpecialCharacters.Right, "f")
def next_slide(state: State) -> None:
    state.next_slide()


@input_handler(SpecialCharacters.Left, "b")
def previous_slide(state: State) -> None:
    state.previous_slide()


@input_handler(SpecialCharacters.Up, modes=[Mode.DECK])
def up_grid_row(state: State) -> None:
    state.previous_slide(move=state.deck_grid_width)


@input_handler(SpecialCharacters.Down, modes=[Mode.DECK])
def down_grid_row(state: State) -> None:
    state.next_slide(move=state.deck_grid_width)


@input_handler("j")
def jump_to_slide(state: State) -> None:
    slide_number = ""

    def display() -> None:
        state.set_message(Text(f"Jumping to slide {slide_number}..."))

    display()

    while True:
        char = get_character(sys.stdin)

        if char is SpecialCharacters.Backspace:
            slide_number = slide_number[:-1]
        elif char is SpecialCharacters.Enter:
            state.current_slide_idx = int(slide_number) - 1
            state.clear_message()
            return
        elif isinstance(char, SpecialCharacters):
            continue
        elif char in string.digits:
            slide_number += char

        display()

        if len(slide_number) == len(str(len(state.deck))):
            state.current_slide_idx = int(slide_number) - 1
            state.clear_message()
            return


@input_handler("d")
def deck_mode(state: State) -> None:
    state.mode = Mode.DECK


@input_handler("s")
def slide_mode(state: State) -> None:
    state.mode = Mode.SLIDE


@input_handler(SpecialCharacters.CtrlK)
def kill(state: State) -> None:
    raise Exit(code=0)
