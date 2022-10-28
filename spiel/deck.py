from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from rich.console import RenderableType


@dataclass
class Slide:
    title: str
    content: Callable[[], RenderableType]
    dynamic: bool


@dataclass
class Deck:
    name: str
    slides: list[slide] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.slides)

    def slide(
        self,
        title: str = "",
        dynamic: bool = False,
    ):
        def slideify(content: Callable[[], RenderableType]) -> Slide:
            slide = Slide(title=title, content=content, dynamic=dynamic)
            self.slides.append(slide)
            return slide

        return slideify
