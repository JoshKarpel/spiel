from __future__ import annotations

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
    lines, _ = inspect.getsourcelines(function)

    prev_indent = None
    for idx, line in enumerate(lines):
        if prev_indent is None:
            prev_indent = count_leading_whitespace(line)
        elif count_leading_whitespace(line) > prev_indent:
            lines = lines[idx:]

    return dedent("".join(lines))


def count_leading_whitespace(s: str) -> int:
    return len(s) - len(s.lstrip())
