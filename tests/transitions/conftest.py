import pytest
from textual.widget import Widget


@pytest.fixture()
def from_widget() -> Widget:
    return Widget()


@pytest.fixture()
def to_widget() -> Widget:
    return Widget()
