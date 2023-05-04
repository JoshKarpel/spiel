from __future__ import annotations

from collections.abc import Iterable

import pytest

from spiel.utils import filter_join


@pytest.mark.parametrize(
    ("joiner", "items", "expected"),
    [
        (".", ["a", "b"], "a.b"),
        (".", ("a", "b"), "a.b"),
        (".", iter(["a", "b"]), "a.b"),
        (".", iter(["a", "", "b"]), "a.b"),
        (".", iter(["a", None, "b"]), "a.b"),
    ],
)
def test_filter_join(joiner: str, items: Iterable[str | None], expected: str) -> None:
    assert filter_join(joiner, items) == expected
