from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Union

from rich.console import ConsoleRenderable
from rich.text import Text

from .presentable import Presentable
from .triggers import Triggers

MakeRenderable = Callable[..., ConsoleRenderable]
RenderableLike = Union[MakeRenderable, ConsoleRenderable]


@dataclass
class Slide(Presentable):
    content: RenderableLike = field(default_factory=Text)

    def render(self, triggers: Triggers) -> ConsoleRenderable:
        if callable(self.content):
            signature = inspect.signature(self.content)

            kwargs: Dict[str, Any] = {}
            if "triggers" in signature.parameters:
                kwargs["triggers"] = triggers

            return self.content(**kwargs)
        else:
            return self.content
