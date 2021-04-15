from dataclasses import dataclass, field
from functools import cached_property
from time import monotonic
from typing import Iterator, Tuple


@dataclass(frozen=True)
class Triggers:
    times: Tuple[float, ...]
    now: float = field(default_factory=monotonic)

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
