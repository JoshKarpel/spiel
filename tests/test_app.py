import pytest

from spiel.app import SpielApp
from spiel.constants import DEMO_FILE


@pytest.fixture
def app() -> SpielApp:
    return SpielApp(
        deck_path=DEMO_FILE,
        _enable_transitions=False,
        _slide_refresh_rate=1 / 10,
    )


async def test_advance_through_demo_slides(app: SpielApp) -> None:
    async with app.run_test() as pilot:
        keys = ("right",) * (len(app.deck) + 1)

        await pilot.press(*keys)

        assert app.current_slide_idx == len(app.deck) - 1
