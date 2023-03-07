import inspect
from collections.abc import Callable
from contextlib import redirect_stdout
from dataclasses import dataclass
from io import StringIO

from rich.console import RenderableType
from rich.panel import Panel
from rich.syntax import Syntax


def example(**kwargs):
    def deco(func):
        return Example(**kwargs, func=func)

    return deco


@dataclass
class Example:
    name: str
    func: Callable[[], None]
    result: str | None = None
    return_value: object = None

    def source_panel(self) -> RenderableType:
        source_lines, _ = inspect.getsourcelines(self.func)
        return Panel.fit(
            Syntax(
                "\n".join(source_lines).rstrip(),
                lexer="python",
            ),
        )

    def results_panel(self) -> RenderableType:
        return Panel.fit(self.result or "")

    def run(self):
        if self.result is not None:
            return

        cap = StringIO()
        with redirect_stdout(cap):
            self.return_value = self.func()

        self.result = cap.getvalue()
