from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from functools import cached_property
from itertools import islice
from time import monotonic
from typing import Iterator, TypeVar, overload

T = TypeVar("T")


@dataclass(frozen=True)
class Triggers(Sequence[float]):
    """
    Provides information to [`Slide.content`][spiel.Slide.content] about the current slide's "trigger state".

    `Triggers` is a [`Sequence`][collections.abc.Sequence] of times
    (produced by [`time.monotonic`][time.monotonic])
    that the current slide was triggered at.
    Note that the slide will be triggered once when it starts being displayed,
    so the first trigger time will be the time when the slide started being displayed.
    """

    now: float
    """
    The time that the slide content is being rendered at.
    Use this is as a single consistent value to base relative times on.
    """

    _times: tuple[float, ...]

    def __post_init__(self) -> None:
        if not self._times:
            raise ValueError("times must not be empty")

        if self.now < self._times[-1]:
            raise ValueError(f"now {self.now} must be later than the last time {self._times[-1]}")

    @classmethod
    def new(self) -> Triggers:
        now = monotonic()
        return Triggers(now=now, _times=(now,))

    def __len__(self) -> int:
        return len(self._times)

    @overload
    def __getitem__(self, item: int) -> float:
        return self._times[item]

    @overload
    def __getitem__(self, item: slice) -> Sequence[float]:
        return self._times[item]

    def __getitem__(self, item: int | slice) -> float | Sequence[float]:
        return self._times[item]

    def __iter__(self) -> Iterator[float]:
        return iter(self._times)

    def __contains__(self, item: object) -> bool:
        return item in self._times

    @cached_property
    def time_since_last_trigger(self) -> float:
        """The elapsed time since the most recent trigger."""
        return self.now - self._times[-1]

    @cached_property
    def time_since_first_trigger(self) -> float:
        """
        The elapsed time since the first trigger,
        which is equivalent to the time since the slide started being displayed.
        """
        return self.now - self._times[0]

    @cached_property
    def triggered(self) -> bool:
        """
        Returns whether the slide has been *manually* triggered
        (i.e., this ignores the initial trigger from when the slide starts being displayed).
        """
        return len(self) > 1

    def take(self, iter: Iterable[T], offset: int = 1) -> Iterator[T]:
        """
        Takes elements from the iterable `iter`
        equal to the number of times in the `Triggers` minus the offset.

        Args:
            iter: The iterable to take elements from.
            offset: This `offset` will be subtracted from the number of triggers,
                reducing the number of elements that will be returned.
                It defaults to `1` to ignore the automatic trigger from when the
                slide starts being shown.

        Returns:
            An iterator over the first `len(self) - offset` elements of `iter`.
        """
        return islice(iter, len(self) - offset)
