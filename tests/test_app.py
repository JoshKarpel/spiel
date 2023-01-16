from collections.abc import Iterable
from itertools import combinations_with_replacement

import pytest
from hypothesis import given
from hypothesis.strategies import lists, sampled_from

import spiel.constants
from spiel.app import SpielApp


@pytest.fixture
def app() -> SpielApp:
    return SpielApp(deck_path=spiel.constants.DEMO_FILE)


KEYS = [
    "right",
    "left",
    "d",
    "t",
    "enter",
    "up",
    "down",
    "escape",
    "question_mark",
]


@pytest.mark.slow
@given(keys=lists(elements=sampled_from(KEYS), max_size=100))
async def test_hammer_on_the_keyboard_long_random(keys: Iterable[str]) -> None:
    app = SpielApp(deck_path=spiel.constants.DEMO_FILE)
    async with app.run_test() as pilot:
        await pilot.press(*keys)


@pytest.mark.slow
@pytest.mark.parametrize("keys", combinations_with_replacement(KEYS, 3))
async def test_hammer_on_the_keyboard_short_exhaustive(app: SpielApp, keys: Iterable[str]) -> None:
    async with app.run_test() as pilot:
        await pilot.press(*keys)


async def test_advance_through_demo_slides(app: SpielApp) -> None:
    async with app.run_test() as pilot:
        keys = ("right",) * (len(app.deck) + 1)

        await pilot.press(*keys)

        assert app.current_slide_idx == len(app.deck) - 1
