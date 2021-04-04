from collections import deque
from time import monotonic
from typing import Deque, Optional

from spiel.constants import TARGET_RPS


class RPSCounter:
    def __init__(self, render_history_length: Optional[int] = None) -> None:
        if render_history_length is None:
            render_history_length = 3 * TARGET_RPS

        self.render_time_history: Deque[float] = deque(maxlen=render_history_length)

    def mark(self) -> None:
        self.render_time_history.append(monotonic())

    def renders_per_second(self) -> float:
        num_samples = len(self.render_time_history)
        if num_samples < 2:
            return 0

        return num_samples / (self.render_time_history[-1] - self.render_time_history[0])

    def seconds_per_render(self) -> float:
        return 1 / self.renders_per_second()
