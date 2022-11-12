from __future__ import annotations

import inspect
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from rich.console import RenderableType
from rich.text import Text

from spiel.triggers import Triggers

TRIGGERS = "triggers"

Content = Callable[..., RenderableType]


@dataclass
class Slide:
    title: str = ""
    content: Content = lambda: Text()
    edit_target: Path | None = None

    def render(self, triggers: Triggers) -> RenderableType:
        signature = inspect.signature(self.content)

        kwargs: dict[str, object] = {}
        if TRIGGERS in signature.parameters:
            kwargs[TRIGGERS] = triggers

        return self.content(**kwargs)
