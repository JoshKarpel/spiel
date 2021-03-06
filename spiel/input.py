from __future__ import annotations

import code
import contextlib
import os
import string
import sys
import termios
from contextlib import contextmanager
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum, unique
from io import UnsupportedOperation
from itertools import product
from pathlib import Path
from typing import (
    Any,
    Callable,
    Iterable,
    Iterator,
    List,
    MutableMapping,
    NoReturn,
    Optional,
    TextIO,
    Tuple,
    Union,
)

import typer
from rich.control import Control
from rich.text import Text
from typer import Exit

from .constants import PACKAGE_NAME
from .example import Example
from .exceptions import DuplicateInputHandler
from .modes import Mode
from .state import State

LFLAG = 3
CC = 6

try:
    ORIGINAL_TCGETATTR: Optional[List[Any]] = termios.tcgetattr(sys.stdin)
except (UnsupportedOperation, termios.error):
    ORIGINAL_TCGETATTR = None


@contextmanager
def no_echo() -> Iterator[None]:
    try:
        start_no_echo(sys.stdin)
        yield
    finally:
        reset_tty(sys.stdin)


def start_no_echo(stream: TextIO) -> None:
    if ORIGINAL_TCGETATTR is None:
        return

    mode = deepcopy(ORIGINAL_TCGETATTR)

    mode[LFLAG] = mode[LFLAG] & ~(termios.ECHO | termios.ICANON)
    mode[CC][termios.VMIN] = 1
    mode[CC][termios.VTIME] = 0

    termios.tcsetattr(stream.fileno(), termios.TCSADRAIN, mode)


def reset_tty(stream: TextIO) -> None:
    if ORIGINAL_TCGETATTR is None:
        return

    termios.tcsetattr(stream.fileno(), termios.TCSADRAIN, ORIGINAL_TCGETATTR)


@unique
class SpecialCharacters(Enum):
    Up = "↑"
    Down = "↓"
    Right = "→"
    Left = "←"
    CtrlUp = "ctrl-up"
    CtrlDown = "ctrl-down"
    CtrlRight = "ctrl-right"
    CtrlLeft = "ctrl-left"
    CtrlK = "ctrl-k"
    CtrlC = "ctrl-c"
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


@dataclass(frozen=True)
class InputHandlerHelpInfo:
    name: str
    help: str
    characters: Tuple[Character, ...]
    modes: List[Mode]


INPUT_HANDLER_HELP: List[InputHandlerHelpInfo] = []


def handle_input(
    state: State,
    stream: TextIO,
    handlers: InputHandlers = INPUT_HANDLERS,
) -> Optional[NoReturn]:
    character = get_character(stream)

    try:
        handler = handlers[(character, state.mode)]
    except KeyError:
        return None

    return handler(state)


def input_handler(
    *characters: Character,
    modes: Optional[Iterable[Mode]] = None,
    handlers: InputHandlers = INPUT_HANDLERS,
    name: Optional[str] = None,
    help: str,
) -> InputHandlerDecorator:
    target_modes = list(modes or list(Mode))

    def decorator(func: InputHandler) -> InputHandler:
        for character, mode in product(characters, target_modes):
            key: InputHandlerKey = (character, mode)
            if key in handlers:
                raise DuplicateInputHandler(
                    f"{character} is already registered as an input handler for mode {mode}"
                )
            handlers[key] = func

        INPUT_HANDLER_HELP.append(
            InputHandlerHelpInfo(
                name=name or " ".join(word.capitalize() for word in func.__name__.split("_")),
                help=help,
                characters=characters,
                modes=target_modes,
            )
        )

        return func

    return decorator


NOT_HELP = [Mode.SLIDE, Mode.DECK]


@input_handler(
    "h",
    help=f"Enter {Mode.HELP} mode.",
)
def help_mode(state: State) -> None:
    state.mode = Mode.HELP


@input_handler(
    "s",
    help=f"Enter {Mode.SLIDE} mode.",
)
def slide_mode(state: State) -> None:
    state.mode = Mode.SLIDE


@input_handler(
    "d",
    help=f"Enter {Mode.DECK} mode.",
)
def deck_mode(state: State) -> None:
    state.mode = Mode.DECK


@input_handler(
    SpecialCharacters.Right,
    "f",
    modes=NOT_HELP,
    help="Move to the next slide.",
)
def next_slide(state: State) -> None:
    state.next_slide()


@input_handler(
    SpecialCharacters.Left,
    "b",
    modes=NOT_HELP,
    help="Move to the previous slide.",
)
def previous_slide(state: State) -> None:
    state.previous_slide()


@input_handler(
    SpecialCharacters.Up,
    modes=[Mode.DECK],
    help="Move to the previous deck grid row.",
)
def up_grid_row(state: State) -> None:
    state.previous_slide(move=state.deck_grid_width)


@input_handler(
    SpecialCharacters.Down,
    modes=[Mode.DECK],
    help="Move to the next deck grid row.",
)
def down_grid_row(state: State) -> None:
    state.next_slide(move=state.deck_grid_width)


@input_handler(
    "j",
    modes=NOT_HELP,
    help="Press the action key, then a slide number (e.g., [bold]17[/bold]), then press [bold]enter[/bold], to jump to that slide.",
)
def jump_to_slide(state: State) -> None:
    slide_number = ""

    def display() -> None:
        state.set_message(Text(f"Jumping to slide {slide_number}..."))

    def jump() -> None:
        state.clear_message()
        if slide_number == "":
            return
        state.jump_to_slide(int(slide_number) - 1)
        return

    display()

    while True:
        char = get_character(sys.stdin)

        if char is SpecialCharacters.Backspace:
            slide_number = slide_number[:-1]
        elif char is SpecialCharacters.Enter:
            return jump()
        elif isinstance(char, SpecialCharacters):
            continue
        elif char in string.digits:
            slide_number += char

        display()

        if len(slide_number) == len(str(len(state.deck))):
            return jump()


@input_handler(
    "t",
    modes=[Mode.SLIDE],
    help="Trigger the slide: marks the current time and make it available to the slide's content rendering function.",
)
def trigger(state: State) -> None:
    state.trigger()


@input_handler(
    "r",
    modes=[Mode.SLIDE],
    help="Reset the trigger state to as if the slide just started being displayed.",
)
def reset_trigger(state: State) -> None:
    state.reset_trigger()


@contextlib.contextmanager
def suspend_live(state: State) -> Iterator[None]:
    live = state.console._live

    if live is None:
        yield
        return

    live.stop()
    yield
    live.start(refresh=True)


@input_handler(
    "e",
    modes=[Mode.SLIDE],
    help=f"Open your $EDITOR ([bold]{os.getenv('EDITOR', 'not set')}[/bold]) on the source of an [bold]Example[/bold] slide. If the current slide is not an [bold]Example[/bold], do nothing.",
)
def edit_example(state: State) -> None:
    s = state.current_slide
    if isinstance(s, Example):
        with suspend_live(state):
            s.source = typer.edit(text=s.source, extension=Path(s.name).suffix, require_save=False)
            s.clear_cache()


def has_ipython() -> bool:
    try:
        import IPython

        return True
    except ImportError:
        return False


def has_ipython_help_message() -> str:
    return "[green]it is[/green]" if has_ipython() else "[red]it is not[/red]"


@input_handler(
    "l",
    name="Open REPL",
    modes=NOT_HELP,
    help=f"Open your REPL. Uses [bold]IPython[/bold] if it is installed ({has_ipython_help_message()}), otherwise the standard Python REPL.",
)
def open_repl(state: State) -> None:
    with suspend_live(state):
        reset_tty(sys.stdin)
        state.console.print(Control.clear())
        state.console.print(Control.move_to(0, 0))

        try:
            import IPython
            from traitlets.config import Config

            c = Config()

            c.InteractiveShellEmbed.colors = "Neutral"

            IPython.embed(config=c)
        except ImportError:
            code.InteractiveConsole().interact()

        start_no_echo(sys.stdin)


@input_handler(
    "p",
    help="Toggle profiling information.",
)
def toggle_profiling(state: State) -> None:
    state.toggle_profiling()


@input_handler(
    SpecialCharacters.CtrlK,
    SpecialCharacters.CtrlC,
    help=f"Exit {PACKAGE_NAME}.",
)
def exit(state: State) -> None:
    raise Exit(code=0)
