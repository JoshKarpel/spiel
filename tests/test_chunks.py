from typing import Any, List

import pytest

from spiel.utils import chunks


@pytest.mark.parametrize(
    "items, n, fill, expected",
    [
        ("abcdef", 3, None, [["a", "b", "c"], ["d", "e", "f"]]),
        ("abcde", 3, None, [["a", "b", "c"], ["d", "e", None]]),
        ("", 2, None, []),
    ],
)
def test_chunks(items: List[Any], n: int, fill: Any, expected: List[List[Any]]) -> None:
    assert [list(chunk) for chunk in chunks(items, n)] == expected
