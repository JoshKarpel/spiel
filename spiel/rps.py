from __future__ import annotations

from collections import deque
from time import monotonic
from typing import Deque

from spiel.constants import TARGET_RPS


class RPSCounter:
    def __init__(self, render_history_length: int | None = None) -> None:
        if render_history_length is None:
            render_history_length = 3 * TARGET_RPS

        self.render_time_history: Deque[float] = deque(maxlen=render_history_length)

    @property
    def num_samples(self) -> int:
        return len(self.render_time_history)

    def mark(self) -> None:
        self.render_time_history.append(monotonic())

    def renders_per_second(self) -> float:
        if self.num_samples < 2:
            return 0

        return self.num_samples / (self.render_time_history[-1] - self.render_time_history[0])

    def last_elapsed_render_time(self) -> float:
        if self.num_samples < 2:
            return 0

        return self.render_time_history[-1] - self.render_time_history[-2]
