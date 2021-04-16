from __future__ import annotations

import inspect
import sys
from collections.abc import Collection
from dataclasses import dataclass, field
from textwrap import dedent
from typing import Callable, Iterator, List, Sequence

from .example import Example
from .presentable import Presentable
from .slides import MakeRenderable, Slide


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
    ) -> Callable[[MakeRenderable], MakeRenderable]:
        def slideify(content: MakeRenderable) -> MakeRenderable:
            slide = Slide(content=content, title=title)
            self.add_slides(slide)
            return content

        return slideify

    def example(
        self,
        title: str = "",
        command: Sequence[str] = (sys.executable,),
        name: str = "example.py",
        language: str = "python",
    ) -> Callable[[Callable], Callable]:
        def exampleify(example: Callable) -> Callable:
            ex = Example(
                source=get_function_body(example),
                title=title,
                command=command,
                name=name,
                language=language,
            )
            self.add_slides(ex)
            return example

        return exampleify


def get_function_body(function: Callable) -> str:
    lines, _ = inspect.getsourcelines(function)

    prev_indent = None
    for idx, line in enumerate(lines):
        if prev_indent is None:
            prev_indent = count_leading_whitespace(line)
        elif count_leading_whitespace(line) > prev_indent:
            return dedent("".join(lines[idx:]))

    raise ValueError(f"Could not extract function body from {function}")


def count_leading_whitespace(s: str) -> int:
    return len(s) - len(s.lstrip())
