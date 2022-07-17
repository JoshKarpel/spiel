from __future__ import annotations

import dis
import inspect
import sys
from collections.abc import Callable, Collection, Iterator, Sequence
from dataclasses import dataclass, field
from textwrap import dedent

from spiel.example import Example
from spiel.presentable import Presentable
from spiel.slide import MakeRenderable, Slide


@dataclass
class Deck(Collection[Presentable]):
    name: str
    slides: list[Presentable] = field(default_factory=list)

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
    ) -> Callable[[MakeRenderable], Slide]:
        def slideify(content: MakeRenderable) -> Slide:
            slide = Slide(
                title=title,
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
    ) -> Callable[[Callable[[], None]], Example]:
        def exampleify(example: Callable[[], None]) -> Example:
            ex = Example(
                title=title,
                source=get_function_body(example),
                command=command,
                name=name,
                language=language,
            )
            self.add_slides(ex)
            return ex

        return exampleify


def get_function_body(function: Callable[..., object]) -> str:
    lines, line_of_def_start = inspect.getsourcelines(function)
    line_of_first_instruction = list(dis.Bytecode(function))[0].starts_line or line_of_def_start
    offset = line_of_first_instruction - line_of_def_start
    return dedent("".join(lines[offset:]))


def count_leading_whitespace(s: str) -> int:
    return len(s) - len(s.lstrip())
