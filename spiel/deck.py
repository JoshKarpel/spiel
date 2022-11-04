from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from typing import Callable, Iterator

from rich.console import RenderableType
from rich.text import Text

from spiel.triggers import Triggers

Content = Callable[[], RenderableType]


@dataclass
class Slide:
    title: str = ""
    content: Callable[..., RenderableType] = lambda: Text()

    def render(self, triggers: Triggers) -> RenderableType:
        signature = inspect.signature(self.content)

        kwargs: dict[str, object] = {}
        if "triggers" in signature.parameters:
            kwargs["triggers"] = triggers

        return self.content(**kwargs)


@dataclass
class Deck:
    name: str
    slides: list[Slide] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.slides)

    def __getitem__(self, item: int) -> Slide:
        return self.slides[item]

    def __iter__(self) -> Iterator[Slide]:
        yield from self.slides

    def slide(
        self,
        title: str = "",
    ) -> Callable[[Content], Slide]:
        def slideify(content: Content) -> Slide:
            slide = Slide(title=title, content=content)
            self.slides.append(slide)
            return slide

        return slideify

    def add_slides(self, *slides: Slide) -> None:
        self.slides.extend(slides)
