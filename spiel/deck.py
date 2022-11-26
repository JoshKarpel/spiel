from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterator, Mapping

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
        bindings: Mapping[str, Callable[[], None]] | None = None,
    ) -> Callable[[Content], Slide]:
        def slideify(content: Content) -> Slide:
            slide = Slide(
                title=title,
                content=content,
                bindings=bindings or {},
            )
            self.add_slides(slide)
            return slide

        return slideify

    def add_slides(self, *slides: Slide) -> None:
        self.slides.extend(slides)
