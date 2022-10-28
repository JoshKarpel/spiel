from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from rich.console import RenderableType

Content = Callable[[], RenderableType]


@dataclass
class Slide:
    title: str
    content: Callable[[], RenderableType]
    dynamic: bool


@dataclass
class Deck:
    name: str
    slides: list[Slide] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.slides)

    def slide(
        self,
        title: str = "",
        dynamic: bool = False,
    ) -> Callable[[Content], Slide]:
        def slideify(content: Content) -> Slide:
            slide = Slide(title=title, content=content, dynamic=dynamic)
            self.slides.append(slide)
            return slide

        return slideify
