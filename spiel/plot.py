import re
from functools import lru_cache
from typing import Any, Iterable, Sequence, Union

import numpy as np
import uniplot
from colorama import Fore
from colorama import Style as CStyle
from rich.console import Console, ConsoleOptions
from rich.segment import Segment
from rich.style import Style
from rich.text import Text

Plottable = Union[
    np.ndarray,
    Sequence[np.ndarray],
]

RE_ANSI_ESCAPE = re.compile(r"(\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~]))")

COLOR_MAP = {
    Fore.RED: "red",
    Fore.GREEN: "green",
    Fore.BLUE: "blue",
    Fore.CYAN: "cyan",
    Fore.YELLOW: "yellow",
    Fore.MAGENTA: "magenta",
    Fore.BLACK: "black",
    Fore.WHITE: "white",
}


class Plot:
    def __init__(self, **plot_args: Any) -> None:
        self.plot_args = plot_args

    def _ansi_to_text(self, s: str) -> Text:
        pieces = []
        tmp = ""
        style = Style.null()
        for char in RE_ANSI_ESCAPE.split(s):
            if char == CStyle.RESET_ALL:
                pieces.append(Text(tmp, style=style))
                style = Style.null()
                tmp = ""
            elif char in COLOR_MAP:
                pieces.append(Text(tmp, style=style))
                style = Style(color=COLOR_MAP[char])
                tmp = ""
            else:
                tmp += char

        # catch leftovers
        pieces.append(Text(tmp, style=style))

        return Text("", no_wrap=True).join(pieces)

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> Iterable[Segment]:
        if self.plot_args.get("height") is None and options.height is None:
            height = None
        else:
            # 5 = title + top bar + bottom bar + bottom axis labels + 1
            height = max(
                (options.height - 5) if options.height else 1, self.plot_args.get("height", 1)
            )

        plot_args = {
            **self.plot_args,
            **dict(
                height=height,
                width=max(options.max_width - 10, self.plot_args.get("width", 1)),
            ),
        }

        plot = "\n".join(uniplot.plot_to_string(**plot_args))

        text = self._ansi_to_text(plot)

        yield from text.__rich_console__(console, options)
