from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from typing import Callable, Mapping

from rich.console import RenderableType
from rich.text import Text

from spiel.triggers import Triggers

TRIGGERS = "triggers"

Content = Callable[..., RenderableType]


@dataclass
class Slide:
    title: str = ""
    content: Content = lambda: Text()
    bindings: Mapping[str, Callable[[], None]] = field(default_factory=dict)

    def render(self, triggers: Triggers) -> RenderableType:
        signature = inspect.signature(self.content)

        kwargs: dict[str, object] = {}
        if TRIGGERS in signature.parameters:
            kwargs[TRIGGERS] = triggers

        return self.content(**kwargs)
