from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Union

from rich.console import ConsoleRenderable, RichCast
from rich.text import Text

Renderable = Union[RichCast, ConsoleRenderable]
MakeRenderable = Callable[[], Renderable]


@dataclass
class Slide:
    content: Renderable = field(default_factory=Text)
    title: str = ""

    @classmethod
    def from_function(
        cls,
        function: MakeRenderable,
        title: str = "",
    ) -> Slide:
        class Dynamic:
            def __rich__(self) -> Renderable:
                return function()

        return cls(content=Dynamic(), title=title)


@dataclass
class Deck:
    name: str
    slides: List[Slide] = field(default_factory=list)

    def __getitem__(self, idx: int) -> Slide:
        return self.slides[idx]

    def __len__(self) -> int:
        return len(self.slides)

    def add_slides(self, *slides: Slide) -> Deck:
        self.slides.extend(slides)
        return self

    def slide(
        self,
        title: str = "",
        dynamic: bool = False,
    ) -> Callable[[MakeRenderable], MakeRenderable]:
        def decorator(slide_function: MakeRenderable) -> MakeRenderable:
            if dynamic:
                slide = Slide.from_function(slide_function, title=title)
            else:
                slide = Slide(slide_function(), title=title)
            self.add_slides(slide)
            return slide_function

        return decorator
