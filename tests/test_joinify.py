from typing import Any, Iterable, Optional

import pytest

from spiel.utils import joinify


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
def test_joinify(joiner: str, items: Iterable[Optional[Any]], expected: str) -> None:
    assert joinify(joiner, items) == expected
