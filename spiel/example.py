from __future__ import annotations

import shlex
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from subprocess import PIPE, STDOUT, CompletedProcess, run
from typing import Callable, NamedTuple, Optional, Sequence

from rich.align import Align
from rich.console import ConsoleRenderable
from rich.layout import Layout
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

from .presentable import Presentable
from .triggers import Triggers


class ImageSize(NamedTuple):
    width: int
    height: int


@dataclass
class CachedExample:
    trigger_number: int
    input: Syntax
    output: Optional[Text]


@dataclass
class Example(Presentable):
    source: str = ""
    command: Sequence[str] = field(default_factory=lambda: [sys.executable])
    name: str = "example.py"
    language: str = "python"
    layout: Optional[Callable[[Syntax, Optional[Text]], ConsoleRenderable]] = None

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

    def _render(self, input: Syntax, output: Optional[Text]) -> ConsoleRenderable:
        if self.layout is None:
            root = Layout()
            root.split_column(
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
                            output,
                            title=f"{shlex.join([Path(self.command[0]).stem, *self.command[1:], self.name])}",
                            title_align="left",
                            expand=False,
                        )
                        if output is not None
                        else Text(" ")
                    )
                ),
            )
            return root
        else:
            return self.layout(input, output)

    def clear_output(self) -> None:
        self._cache = None

    def render(self, triggers: Triggers) -> ConsoleRenderable:
        if self._cache is None:
            self._cache = CachedExample(len(triggers), self.input(), None)
        if self._cache.trigger_number != len(triggers):
            self._cache = CachedExample(len(triggers), self.input(), self.output())

        return self._render(self._cache.input, self._cache.output)
