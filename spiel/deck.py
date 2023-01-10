from __future__ import annotations

from collections.abc import Callable, Iterator, Mapping, Sequence
from dataclasses import dataclass, field
from typing import overload

from spiel.slide import Content, Slide


@dataclass
class Deck(Sequence[Slide]):
    """
    Represents a "deck" of "slides": a presentation.
    """

    name: str
    """The name of the `Deck`/presentation, which will be displayed in the footer."""

    _slides: list[Slide] = field(default_factory=list)

    def slide(
        self,
        title: str = "",
        bindings: Mapping[str, Callable[..., None]] | None = None,
    ) -> Callable[[Content], Content]:
        """
        A decorator that creates a new slide in the deck,
        with the decorated function as the `Slide`'s `content`.

        Args:
            title: The title to display for the slide.
            bindings: A mapping of
                [keys](https://textual.textualize.io/guide/input/#key)
                to callables to be executed when those keys are pressed,
                when on this slide.
        """

        def slideify(content: Content) -> Content:
            slide = Slide(
                title=title,
                content=content,
                bindings=bindings or {},
            )
            self.add_slides(slide)
            return content

        return slideify

    def add_slides(self, *slides: Slide) -> None:
        """
        Add `Slide`s to a `Deck`.

        This function is primarily useful when adding multiple slides at once,
        probably generated programmatically.
        If adding a single slide, prefer the [`Deck.slide`][spiel.Deck.slide] decorator.

        Args:
            *slides: The `Slide`s to add.
        """
        self._slides.extend(slides)

    def __len__(self) -> int:
        return len(self._slides)

    @overload
    def __getitem__(self, item: int) -> Slide:
        return self._slides[item]

    @overload
    def __getitem__(self, item: slice) -> Sequence[Slide]:
        return self._slides[item]

    def __getitem__(self, item: int | slice) -> Slide | Sequence[Slide]:
        return self._slides[item]

    def __iter__(self) -> Iterator[Slide]:
        yield from self._slides

    def __contains__(self, item: object) -> bool:
        return item in self._slides
