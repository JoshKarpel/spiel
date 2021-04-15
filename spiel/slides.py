from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterator, List, Union

from rich.console import ConsoleRenderable
from rich.text import Text

from .triggers import Triggers

MakeRenderable = Callable[..., ConsoleRenderable]
RenderableLike = Union[MakeRenderable, ConsoleRenderable]


@dataclass
class Presentable:  # Why not an ABC? https://github.com/python/mypy/issues/5374
    title: str = ""

    def render(self, triggers: Triggers) -> ConsoleRenderable:
        raise NotImplementedError


@dataclass
class Slide(Presentable):
    content: RenderableLike = field(default_factory=Text)

    def render(self, triggers: Triggers) -> ConsoleRenderable:
        if callable(self.content):
            signature = inspect.signature(self.content)

            kwargs: Dict[str, Any] = {}
            if "triggers" in signature.parameters:
                kwargs["triggers"] = triggers

            return self.content(**kwargs)
        else:
            return self.content


@dataclass
class Deck:
    name: str
    slides: List[Presentable] = field(default_factory=list)

    def __getitem__(self, idx: int) -> Presentable:
        return self.slides[idx]

    def __len__(self) -> int:
        return len(self.slides)

    def __iter__(self) -> Iterator[Presentable]:
        yield from self.slides

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
