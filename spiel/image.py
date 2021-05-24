from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from math import floor
from pathlib import Path
from typing import Iterable, Iterator, List, NamedTuple, Tuple, Union

from PIL import Image as Img
from rich.color import Color
from rich.console import Console, ConsoleOptions
from rich.segment import Segment
from rich.style import Style

from .utils import chunks


class ImageSize(NamedTuple):
    width: int
    height: int


Pixels = Tuple[Union[Tuple[int, int, int], None], ...]


@lru_cache(maxsize=2 ** 8)
def _pixels_to_segments(pixels: Pixels, size: ImageSize) -> List[Segment]:
    line = Segment.line()

    segments = []
    pixel_row_pairs = chunks(chunks(pixels, size.width), 2, fill_value=[None] * size.width)
    for top_pixel_row, bottom_pixel_row in pixel_row_pairs:
        for top_pixel, bottom_pixel in zip(top_pixel_row, bottom_pixel_row):
            # use upper-half-blocks for the top pixel row and the background color for the bottom pixel row
            segments.append(
                Segment(
                    text="▀",
                    style=Style(
                        color=Color.from_rgb(*top_pixel) if top_pixel else None,
                        bgcolor=Color.from_rgb(*bottom_pixel) if bottom_pixel else None,
                    ),
                )
            )
        segments.append(line)

    return list(Segment.simplify(segments))


@lru_cache(maxsize=2 ** 4)
def _load_image(path: Path) -> Image:
    return Img.open(path)


@dataclass(frozen=True)
class Image:
    img: Img

    @classmethod
    def from_file(cls, path: Path) -> Image:
        return cls(img=_load_image(path))

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
        pixels = tuple(resized.getdata())
        yield from _pixels_to_segments(pixels, size)
