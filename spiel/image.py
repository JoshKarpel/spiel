from __future__ import annotations

from dataclasses import dataclass
from math import floor
from pathlib import Path
from typing import Iterable, NamedTuple

from PIL import Image as Img
from rich.color import Color
from rich.console import Console, ConsoleOptions, JustifyMethod
from rich.segment import Segment
from rich.style import Style
from rich.text import Text

from spiel.utils import chunks


class ImageSize(NamedTuple):
    width: int
    height: int


@dataclass(frozen=True)
class Image:
    img: Img
    justify: JustifyMethod = "center"

    @classmethod
    def from_file(cls, path: Path, justify: JustifyMethod = "center") -> Image:
        return cls(img=Img.open(path), justify=justify)

    def _determine_size(self, options: ConsoleOptions) -> ImageSize:
        width, height = self.img.size

        # multiply the max height by 2, because we're going to print 2 "pixels" per row
        max_height = options.height * 2 if options.height else None
        if max_height:
            width, height = width * max_height / self.img.height, max_height

        if width > options.max_width:
            width, height = options.max_width, height * options.max_width / width

        return ImageSize(floor(width), floor(height))

    def _resize(self, size: ImageSize) -> Img:
        return self.img.resize(
            size=size,
            resample=Img.LANCZOS,
        )

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> Iterable[Segment]:
        size = self._determine_size(options)
        resized = self._resize(size)

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
