import inspect
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Mapping, Optional

from rich.console import ConsoleRenderable

from .triggers import Triggers


@dataclass
class Presentable:  # Why not an ABC? https://github.com/python/mypy/issues/5374
    title: str = ""
    notebook: Optional[Path] = None

    def render(self, triggers: Triggers) -> ConsoleRenderable:
        raise NotImplementedError

    def get_render_kwargs(self, function: Callable, triggers: Triggers) -> Mapping[str, Any]:
        signature = inspect.signature(function)

        kwargs: Dict[str, Any] = {}
        if "triggers" in signature.parameters:
            kwargs["triggers"] = triggers

        return kwargs
