from dataclasses import dataclass
from functools import cached_property
from math import floor
from pathlib import Path
from typing import Iterable, NamedTuple

from PIL import Image as _Image
from rich.color import Color
from rich.console import Console, ConsoleOptions, JustifyMethod
from rich.segment import Segment
from rich.style import Style
from rich.text import Text

from spiel.utils import chunks


class ImageSize(NamedTuple):
    width: int
    height: int


@dataclass
class Image:
    path: Path
    justify: JustifyMethod = "center"

    @cached_property
    def img(self) -> _Image:
        return _Image.open(self.path)

    def _determine_size(self, options: ConsoleOptions) -> ImageSize:
        width, height = self.img.size
        max_height = options.height * 2 if options.height else None
        if max_height:
            width, height = width * max_height / self.img.height, max_height
        if width > options.max_width:
            width, height = options.max_width, height * options.max_width / width

        return ImageSize(floor(width), floor(height))

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> Iterable[Segment]:
        size = self._determine_size(options)

        resized = self.img.resize(
            size=size,
            resample=_Image.LANCZOS,
        )

        rows = [
            [
                Text(
                    "▀",
                    Style(
                        color=Color.from_rgb(*top),
                        bgcolor=Color.from_rgb(*bottom) if bottom else None,
                    ),
                )
                # ... produce one row of text, using upper-half-blocks for the top image row and the background for the bottom image row
                for top, bottom in zip(top_row, bottom_row)
            ]
            # for each pair of rows in the image...
            for top_row, bottom_row in chunks(
                chunks(resized.getdata(), size.width), 2, fill_value=[None] * size.width
            )
        ]

        text = Text("\n", justify=self.justify).join(Text("").join(row) for row in rows)

        yield from text.__rich_console__(console, options)
