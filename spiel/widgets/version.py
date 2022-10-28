from __future__ import annotations

from rich.console import RenderableType
from textual.widget import Widget


class DebugInfo(Widget):
    DEFAULT_CSS = """
    VersionPanel {
        width: auto;
        height: auto;
    }
    """

    def render(self) -> RenderableType:
        return
