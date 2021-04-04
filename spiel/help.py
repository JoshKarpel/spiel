from dataclasses import dataclass
from textwrap import dedent

from rich.align import Align
from rich.console import Console, ConsoleRenderable, RenderGroup
from rich.markdown import Markdown
from rich.padding import Padding
from rich.style import Style
from rich.table import Column, Table
from rich.text import Text

from spiel.constants import PACKAGE_NAME, __python_version__, __rich_version__, __version__
from spiel.input import INPUT_HANDLER_HELP, SpecialCharacters
from spiel.modes import Mode
from spiel.state import State


@dataclass
class Help:
    state: State

    def __rich__(self) -> ConsoleRenderable:
        markup = dedent(
            """\
            ## Help

            There are a variety of *actions* that you can use to control Spiel during a presentation.

            Each action is triggered by pressing one of a certain set of keys (like `j`) or combinations of keys (like `ctrl-k`).
            Some actions may only be available in certain modes.
            """
        )

        action_table = Table(
            Column(
                "Action",
                style=Style(bold=True),
            ),
            Column(
                "Keys",
                style=Style(bold=True),
                justify="center",
            ),
            Column(
                "Modes",
                justify="center",
            ),
            Column(
                "Description",
            ),
            show_lines=True,
        )

        for info in INPUT_HANDLER_HELP:
            action_table.add_row(
                Text(info.name),
                Text("  ").join(
                    Text(c.value if isinstance(c, SpecialCharacters) else c)
                    for c in info.characters
                ),
                Text(", ").join(Text(mode.value) for mode in info.modes)
                if len(info.modes) != len(list(Mode))
                else Text("any", style=Style(italic=True)),
                Text.from_markup(info.help),
            )

        return Padding(
            RenderGroup(
                Markdown(markup, justify="center"),
                Align(action_table, align="center"),
                Align(version_details(self.state.console), align="center"),
            ),
            pad=(0, 1),
        )


def version_details(console: Console) -> ConsoleRenderable:
    table = Table(
        Column(justify="right"),
        Column(justify="left"),
        show_header=False,
        box=None,
    )

    table.add_row(f"{PACKAGE_NAME.capitalize()} Version", __version__)
    table.add_row("Rich Version", __rich_version__)
    table.add_row("Python Version", __python_version__, end_section=True)
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

    return table
