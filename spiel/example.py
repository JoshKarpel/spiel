from __future__ import annotations

import shlex
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from subprocess import PIPE, STDOUT, run
from typing import Callable, Optional, Sequence

from rich.align import Align
from rich.console import ConsoleRenderable
from rich.layout import Layout
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

from .presentable import Presentable
from .triggers import Triggers


@dataclass
class CachedExample:
    trigger_number: int
    input: str
    output: Optional[str]


def example_panels(example: Example) -> ConsoleRenderable:
    root = Layout()
    root.split_column(
        Layout(
            Align.center(
                Panel(
                    example.input,
                    title=example.name,
                    title_align="left",
                    expand=False,
                )
            )
        ),
        Layout(
            Align.center(
                Panel(
                    example.output,
                    title=f"$ {example.display_command}",
                    title_align="left",
                    expand=False,
                )
                if example.output is not None
                else Text(" ")
            )
        ),
    )
    return root


ExampleLayout = Callable[["Example"], ConsoleRenderable]


@dataclass
class Example(Presentable):
    source: str = ""
    command: Sequence[str] = (sys.executable,)
    name: str = "example.py"
    language: str = "python"
    _layout: ExampleLayout = example_panels
    _cache: Optional[CachedExample] = None

    def layout(self, function: ExampleLayout) -> ExampleLayout:
        self._layout = function
        return function

    @property
    def display_command(self) -> str:
        return shlex.join([Path(self.command[0]).stem, *self.command[1:], self.name])

    def execute(self) -> str:
        with tempfile.TemporaryDirectory() as tmpdir:
            dir = Path(tmpdir)
            file = dir / self.name
            file.write_text(self.source)
            result = run([*self.command, file], stdout=PIPE, stderr=STDOUT, text=True)
        return result.stdout

    @property
    def input(self) -> Syntax:
        input = (self._cache.input or "") if self._cache is not None else ""
        return Syntax(
            input.strip(),
            lexer=self.language,
            code_width=max(len(line) for line in input.splitlines()),
        )

    @property
    def output(self) -> Optional[Text]:
        return (
            Text(self._cache.output)
            if (self._cache is not None and self._cache.output is not None)
            else None
        )

    def clear_cache(self) -> None:
        self._cache = None

    def render(self, triggers: Triggers) -> ConsoleRenderable:
        if self._cache is None:
            self._cache = CachedExample(len(triggers), self.source, None)
        elif self._cache.trigger_number != len(triggers):
            self._cache = CachedExample(len(triggers), self.source, self.execute())

        return self._layout(
            self, **self.get_render_kwargs(function=self._layout, triggers=triggers)
        )
