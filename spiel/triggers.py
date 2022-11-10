from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from time import monotonic
from typing import Iterator


@dataclass(frozen=True)
class Triggers:
    times: tuple[float, ...]
    now: float

    def __post_init__(self) -> None:
        if not self.times:
            raise ValueError("times must not be empty")

        if self.now < self.times[-1]:
            raise ValueError(f"now {self.now} must be later than the last time {self.times[-1]}")

    @classmethod
    def new(self) -> Triggers:
        now = monotonic()
        return Triggers(now=now, times=(now,))

    def __len__(self) -> int:
        return len(self.times)

    def __getitem__(self, idx: int) -> float:
        return self.times[idx]

    def __iter__(self) -> Iterator[float]:
        return iter(self.times)

    @cached_property
    def time_since_last_trigger(self) -> float:
        return self.now - self.times[-1]

    @cached_property
    def time_since_first_trigger(self) -> float:
        return self.now - self.times[0]

    @cached_property
    def triggered(self) -> bool:
        return len(self) > 1
