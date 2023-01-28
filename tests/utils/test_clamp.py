import pytest
from hypothesis import given
from hypothesis import strategies as st

from spiel.utils import clamp


@given(st.tuples(st.integers(), st.integers(), st.integers()).filter(lambda x: x[1] <= x[2]))
def test_clamp(value_lower_upper: tuple[int, int, int]) -> None:
    value, lower, upper = value_lower_upper
    clamped = clamp(value, lower, upper)
    assert lower <= clamped <= upper


@given(st.tuples(st.integers(), st.integers(), st.integers()).filter(lambda x: x[1] > x[2]))
def test_clamp_raises_for_bad_bounds(value_lower_upper: tuple[int, int, int]) -> None:
    value, lower, upper = value_lower_upper
    with pytest.raises(ValueError):
        clamp(value, lower, upper)
