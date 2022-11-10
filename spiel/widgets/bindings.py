from __future__ import annotations

from rich.console import RenderableType
from rich.padding import Padding
from rich.table import Column, Table
from rich.text import Text
from textual.binding import Binding

from spiel.widgets.widget import SpielWidget


class AppBindingsTableWidget(SpielWidget):
    DEFAULT_CSS = """
    AppBindingsTableWidget {
        width: auto;
        height: auto;
    }
    """

    def render(self) -> RenderableType:
        table = Table(
            Column("Key", justify="left"),
            Column("Description", justify="left"),
            title=f"All Views",
        )

        for binding in self.app.BINDINGS:
            if isinstance(binding, Binding):
                table.add_row(binding.key, binding.description)
            else:
                raise TypeError(f"{binding} on {self.app} needs to be a {Binding.__name__}")

        return Padding(table, pad=1)


class ScreenBindingsTableWidget(SpielWidget):
    DEFAULT_CSS = """
    ScreenBindingsTableWidget {
        width: auto;
        height: auto;
    }
    """

    def render(self) -> RenderableType:
        if self.id is None:
            return Text("")

        screen = self.app.get_screen(self.id)
        table = Table(
            Column("Key", justify="left"),
            Column("Description", justify="left"),
            title=f"{self.id.title()} View",
        )

        for binding in screen.BINDINGS:
            if isinstance(binding, Binding):
                table.add_row(binding.key, binding.description)
            else:
                raise TypeError(f"{binding} on {screen} needs to be a {Binding.__name__}")

        return Padding(table, pad=1)
