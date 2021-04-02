from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Union

from rich.console import ConsoleRenderable, RichCast
from rich.text import Text

MakeRenderable = Callable[[], ConsoleRenderable]


@dataclass
class Slide:
    content: ConsoleRenderable = field(default_factory=Text)
    title: str = ""

    @classmethod
    def from_function(
        cls,
        function: MakeRenderable,
        title: str = "",
    ) -> Slide:
        class Dynamic(ConsoleRenderable):
            def __rich__(self) -> ConsoleRenderable:
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
        from_function: bool = False,
    ) -> Callable[[MakeRenderable], MakeRenderable]:
        def decorator(slide_function: MakeRenderable) -> MakeRenderable:
            if from_function:
                slide = Slide.from_function(slide_function, title=title)
            else:
                slide = Slide(slide_function(), title=title)
            self.add_slides(slide)
            return slide_function

        return decorator
