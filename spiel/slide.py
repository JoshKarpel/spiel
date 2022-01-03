from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Union

from rich.console import ConsoleRenderable
from rich.text import Text

from spiel.presentable import Presentable
from spiel.triggers import Triggers

MakeRenderable = Callable[..., ConsoleRenderable]
RenderableLike = Union[MakeRenderable, ConsoleRenderable]


@dataclass
class Slide(Presentable):
    content: RenderableLike = field(default_factory=Text)

    def render(self, triggers: Triggers) -> ConsoleRenderable:
        if callable(self.content):
            return self.content(**self.get_render_kwargs(function=self.content, triggers=triggers))
        else:
            return self.content
