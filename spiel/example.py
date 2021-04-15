from __future__ import annotations

import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from subprocess import CompletedProcess, run, STDOUT, PIPE
from typing import NamedTuple, List, Optional, Callable

import shlex

from rich.align import Align
from rich.console import ConsoleRenderable
from rich.layout import Layout
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

from spiel import Slide


class ImageSize(NamedTuple):
    width: int
    height: int


@dataclass
class CachedExample:
    trigger_number: int
    input: Syntax
    output: Text


NO_OUTPUT = object()


@dataclass
class Example(Slide):
    source: str = ""
    command: List[str] = field(default_factory=lambda: [sys.executable])
    name: str = "example.py"
    language: str = "python"
    layout: Optional[Callable[[Syntax, Text], ConsoleRenderable]] = None

    _cache: Optional[CachedExample] = None

    def input(self) -> Syntax:
        return Syntax(
            self.source,
            lexer_name=self.language,
            code_width=max(len(line) for line in self.source.splitlines()),
        )

    def execute(self) -> CompletedProcess:
        with tempfile.TemporaryDirectory() as tmpdir:
            dir = Path(tmpdir)
            file = dir / self.name
            file.write_text(self.source)
            return run([*self.command, file], stdout=PIPE, stderr=STDOUT, text=True)

    def output(self) -> Text:
        result = self.execute()

        return Text(result.stdout)

    def _render(self, input: Syntax, output: Text) -> ConsoleRenderable:
        if self.layout is None:
            renderable = Layout()
            renderable.split_column(
                Layout(
                    Align.center(
                        Panel(
                            input,
                            title=self.name,
                            title_align="left",
                            expand=False,
                        )
                    )
                ),
                Layout(
                    Align.center(
                        Panel(
                            output if output is not NO_OUTPUT else Text(" "),
                            title=f"{shlex.join([Path(self.command[0]).stem, *self.command[1:], self.name])}",
                            title_align="left",
                            expand=False,
                        )
                        if output is not NO_OUTPUT
                        else Text(" ")
                    )
                ),
            )
        else:
            renderable = self.layout(input, output)
        return renderable

    def clear_output(self):
        self._cache = None

    def render(self, trigger_times: List[float]) -> ConsoleRenderable:
        if self._cache is None:
            self._cache = CachedExample(len(trigger_times), self.input(), NO_OUTPUT)
        if self._cache.trigger_number != len(trigger_times):
            self._cache = CachedExample(len(trigger_times), self.input(), self.output())

        return self._render(self._cache.input, self._cache.output)
