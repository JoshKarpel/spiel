import pickle
import re
from functools import lru_cache
from typing import Any, Iterable, List, Sequence, Union

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

ANSI_COLOR_TO_STYLE = {
    CStyle.RESET_ALL: Style.null(),
    Fore.RED: Style(color="red"),
    Fore.GREEN: Style(color="green"),
    Fore.BLUE: Style(color="blue"),
    Fore.CYAN: Style(color="cyan"),
    Fore.YELLOW: Style(color="yellow"),
    Fore.MAGENTA: Style(color="magenta"),
    Fore.BLACK: Style(color="black"),
    Fore.WHITE: Style(color="white"),
}


@lru_cache(maxsize=2 ** 8)
def _ansi_to_text(s: str) -> List[Segment]:
    segments = []
    tmp = ""
    null_style = Style.null()
    style = null_style
    for char in RE_ANSI_ESCAPE.split(s):
        if char in ANSI_COLOR_TO_STYLE:
            segments.append(Segment(tmp, style=style))
            style = ANSI_COLOR_TO_STYLE[char]
            tmp = ""
        else:
            tmp += char

    # catch leftovers
    segments.append(Segment(tmp, style=style))

    return list(Segment.simplify(segments))


@lru_cache(maxsize=2 ** 8)
def _make_plot(pickled_plot_args: bytes) -> List[str]:
    # This is kind of ugly, but we pickle the args before passing them as an easy
    # way to make them hashable. This helps a lot for performance on static plots,
    # and doesn't have toooooo much impact on dynamic plots.
    return uniplot.plot_to_string(**pickle.loads(pickled_plot_args))


class Plot:
    def __init__(
        self,
        **plot_args: Any,
    ) -> None:
        self.plot_args = plot_args

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

        plot = "\n".join(_make_plot(pickled_plot_args=pickle.dumps(plot_args)))
        # plot = "\n".join(uniplot.plot_to_string(plot_args))

        yield from _ansi_to_text(plot)
