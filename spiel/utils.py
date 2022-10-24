from __future__ import annotations

from collections.abc import Iterable, Iterator
from itertools import zip_longest
from typing import TypeVar

T = TypeVar("T")


def filter_join(separator: str, items: Iterable[object | None]) -> str:
    return separator.join(map(str, filter(None, items)))


def drop_nones(*items: T | None) -> Iterator[T]:
    yield from (item for item in items if item is not None)


def clamp(value: int, lower: int, upper: int) -> int:
    if lower > upper:
        raise ValueError(
            f"Upper bound ({upper}) for clamp must be greater than lower bound ({lower})."
        )
    return max(min(value, upper), lower)


def chunks(iterable: Iterable[T], n: int, fill_value: T | None = None) -> Iterable[Iterable[T]]:
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fill_value)
