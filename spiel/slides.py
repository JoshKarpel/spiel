from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterator, List, Union

from rich.console import ConsoleRenderable
from rich.text import Text

MakeRenderable = Callable[[], ConsoleRenderable]
RenderableLike = Union[MakeRenderable, ConsoleRenderable]


@dataclass
class Slide:
    content: RenderableLike = field(default_factory=Text)
    title: str = ""

    def render(self) -> ConsoleRenderable:
        if callable(self.content):
            return self.content()
        else:
            return self.content


@dataclass
class Deck:
    name: str
    slides: List[Slide] = field(default_factory=list)

    def __getitem__(self, idx: int) -> Slide:
        return self.slides[idx]

    def __len__(self) -> int:
        return len(self.slides)

    def __iter__(self) -> Iterator[Slide]:
        yield from self.slides

    def add_slides(self, *slides: Slide) -> Deck:
        self.slides.extend(slides)
        return self

    def slide(
        self,
        title: str = "",
    ) -> Callable[[MakeRenderable], MakeRenderable]:
        def decorator(slide_function: MakeRenderable) -> MakeRenderable:
            slide = Slide(slide_function, title=title)
            self.add_slides(slide)
            return slide_function

        return decorator
