from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Union

from rich.console import ConsoleRenderable, RichCast
from rich.text import Text


@dataclass
class Slide:
    content: Union[RichCast, ConsoleRenderable] = field(default_factory=Text)
    title: str = ""


@dataclass
class Deck:
    name: str
    slides: List[Slide] = field(default_factory=list)

    def __getitem__(self, idx: int) -> Slide:
        return self.slides[idx]

    def __len__(self) -> int:
        return len(self.slides)

    def add_slide(self, slide: Slide) -> Deck:
        self.slides.append(slide)

        return self
