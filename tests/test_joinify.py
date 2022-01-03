from typing import Any, Iterable, Optional

import pytest

from spiel.utils import filter_join


@pytest.mark.parametrize(
    "joiner, items, expected",
    [
        (".", ["a", "b"], "a.b"),
        (".", ("a", "b"), "a.b"),
        (".", iter(["a", "b"]), "a.b"),
        (".", iter(["a", "", "b"]), "a.b"),
        (".", iter(["a", None, "b"]), "a.b"),
    ],
)
def test_filter_join(joiner: str, items: Iterable[Optional[Any]], expected: str) -> None:
    assert filter_join(joiner, items) == expected
