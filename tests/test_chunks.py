from typing import List, Optional, TypeVar

import pytest

from spiel.utils import chunks

T = TypeVar("T")


@pytest.mark.parametrize(
    "items, n, fill, expected",
    [
        ("abcdef", 3, None, [["a", "b", "c"], ["d", "e", "f"]]),
        ("abcde", 3, None, [["a", "b", "c"], ["d", "e", None]]),
        ("abcde", 3, "fill", [["a", "b", "c"], ["d", "e", "fill"]]),
        ("", 2, None, []),
    ],
)
def test_chunks(items: List[T], n: int, fill: Optional[T], expected: List[List[T]]) -> None:
    assert [list(chunk) for chunk in chunks(items, n, fill_value=fill)] == expected
