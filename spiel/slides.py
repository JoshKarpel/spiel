from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Union

from rich.console import ConsoleRenderable, RichCast
from rich.text import Text

Renderable = Union[RichCast, ConsoleRenderable]
Contentlike = Union[Renderable, Callable[[], Renderable]]


@dataclass
class Slide:
    content: Contentlike = field(default_factory=Text)
    title: str = ""

    def render(self) -> Renderable:
        if callable(self.content):
            return self.content()
        else:
            return self.content

    def __call__(self) -> Slide:
        return self


Slidelike = Union[Slide, Callable[[], Slide]]


@dataclass
class Deck:
    name: str
    _slides: List[Slidelike] = field(default_factory=list)

    @property
    def slides(self) -> List[Slide]:
        return [slide() for slide in self._slides]

    def __getitem__(self, idx: int) -> Slide:
        return self.slides[idx]()

    def __len__(self) -> int:
        return len(self.slides)

    def add_slides(self, *slides: Slidelike) -> Deck:
        self._slides.extend(slides)

        return self
