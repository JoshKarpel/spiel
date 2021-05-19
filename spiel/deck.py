from __future__ import annotations

import dis
import inspect
import sys
from collections.abc import Collection
from dataclasses import dataclass, field
from pathlib import Path
from textwrap import dedent
from typing import Callable, Iterator, List, Optional, Sequence

from .example import Example
from .presentable import Presentable
from .slide import MakeRenderable, Slide


@dataclass
class Deck(Collection):
    name: str
    slides: List[Presentable] = field(default_factory=list)

    def __getitem__(self, idx: int) -> Presentable:
        return self.slides[idx]

    def __len__(self) -> int:
        return len(self.slides)

    def __iter__(self) -> Iterator[Presentable]:
        return iter(self.slides)

    def __contains__(self, obj: object) -> bool:
        return obj in self.slides

    def add_slides(self, *slides: Presentable) -> Deck:
        self.slides.extend(slides)
        return self

    def slide(
        self,
        title: str = "",
        notebook: Optional[Path] = None,
    ) -> Callable[[MakeRenderable], Slide]:
        def slideify(content: MakeRenderable) -> Slide:
            slide = Slide(
                title=title,
                notebook=notebook,
                content=content,
            )
            self.add_slides(slide)
            return slide

        return slideify

    def example(
        self,
        title: str = "",
        command: Sequence[str] = (sys.executable,),
        name: str = "example.py",
        language: str = "python",
        notebook: Optional[Path] = None,
    ) -> Callable[[Callable], Example]:
        def exampleify(example: Callable) -> Example:
            ex = Example(
                title=title,
                notebook=notebook,
                source=get_function_body(example),
                command=command,
                name=name,
                language=language,
            )
            self.add_slides(ex)
            return ex

        return exampleify


def get_function_body(function: Callable) -> str:
    lines, line_of_def_start = inspect.getsourcelines(function)
    line_of_first_instruction = list(dis.Bytecode(function))[0].starts_line or 0
    offset = line_of_first_instruction - line_of_def_start
    return dedent("".join(lines[offset:]))


def count_leading_whitespace(s: str) -> int:
    return len(s) - len(s.lstrip())
