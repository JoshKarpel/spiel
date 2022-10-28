from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterator

from rich.console import RenderableType
from rich.text import Text

Content = Callable[[], RenderableType]


@dataclass
class Slide:
    title: str = ""
    content: Callable[[], RenderableType] = lambda: Text()
    dynamic: bool = False


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
        dynamic: bool = False,
    ) -> Callable[[Content], Slide]:
        def slideify(content: Content) -> Slide:
            slide = Slide(title=title, content=content, dynamic=dynamic)
            self.slides.append(slide)
            return slide

        return slideify

    def add_slides(self, *slides: Slide) -> None:
        self.slides.extend(slides)
