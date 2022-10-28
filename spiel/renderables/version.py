from __future__ import annotations

from rich.console import Console, ConsoleOptions, RenderResult
from rich.style import Style
from rich.table import Column, Table
from rich.text import Text

from spiel import __version__
from spiel.constants import PACKAGE_NAME, __python_version__, __rich_version__, __textual_version__


class DebugTable:
    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        table = Table(
            Column(justify="right"),
            Column(justify="left"),
            show_header=False,
        )

        table.add_row(f"{PACKAGE_NAME.capitalize()} Version", __version__)
        table.add_row("Rich Version", __rich_version__)
        table.add_row("Textual Version", __textual_version__)
        table.add_row("Python Version", __python_version__)

        table.add_section()

        table.add_row(
            "Color System",
            Text(
                console.color_system or "unknown",
                style=Style(color="red" if console.color_system != "truecolor" else "green"),
            ),
        )
        table.add_row(
            "Console Dimensions",
            Text(f"{console.width} cells wide, {console.height} cells tall"),
            end_section=True,
        )

        yield table
