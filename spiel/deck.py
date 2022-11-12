from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterator

from spiel.slide import Content, Slide


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
        edit_target: Path | None = None,
    ) -> Callable[[Content], Slide]:
        def slideify(content: Content) -> Slide:
            slide = Slide(
                title=title,
                content=content,
                edit_target=edit_target,
            )
            self.add_slides(slide)
            return slide

        return slideify

    def add_slides(self, *slides: Slide) -> None:
        self.slides.extend(slides)
