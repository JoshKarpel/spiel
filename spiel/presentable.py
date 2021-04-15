from dataclasses import dataclass

from rich.console import ConsoleRenderable

from .triggers import Triggers


@dataclass
class Presentable:  # Why not an ABC? https://github.com/python/mypy/issues/5374
    title: str = ""

    def render(self, triggers: Triggers) -> ConsoleRenderable:
        raise NotImplementedError
