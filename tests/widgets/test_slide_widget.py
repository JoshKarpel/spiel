import pytest
from pytest import FixtureRequest
from pytest_mock import MockerFixture
from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text

from spiel import Slide
from spiel.widgets.slide import SlideWidget


@pytest.fixture(params=["", Text()])
def slide(request: FixtureRequest) -> Slide:
    def content() -> RenderableType:
        return request.param

    return Slide(content=content)


@pytest.fixture()
def error_slide() -> Slide:
    def content() -> RenderableType:
        raise Exception()

    return Slide(content=content)


@pytest.fixture()
def unrenderable_slide() -> Slide:
    def content() -> None:
        return None

    return Slide(content=content)  # type: ignore[arg-type]


def mock(mocker: MockerFixture, slide: Slide) -> SlideWidget:
    sw = SlideWidget()

    mocker.patch.object(
        type(sw),
        "current_slide",
        new_callable=mocker.PropertyMock,
        return_value=slide,
    )

    assert sw.current_slide is slide

    return sw


def test_render(mocker: MockerFixture, slide: Slide) -> None:
    sw = mock(mocker, slide)

    assert sw.render() == slide.render(triggers=sw.triggers)

    assert "error" not in sw.classes


def test_render_raises_exception(mocker: MockerFixture, error_slide: Slide) -> None:
    sw = mock(mocker, error_slide)

    error = sw.render()

    assert isinstance(error, Panel)
    assert error.title == "Slide content failed to render"

    assert "error" in sw.classes


def test_render_content_not_renderable(mocker: MockerFixture, unrenderable_slide: Slide) -> None:
    sw = mock(mocker, unrenderable_slide)

    error = sw.render()

    assert isinstance(error, Panel)
    assert error.title == "Slide content failed to render"

    assert "error" in sw.classes


def test_update_triggers() -> None:
    sw = SlideWidget()

    initial_triggers = sw.triggers

    sw.update_triggers()

    assert initial_triggers.now <= sw.triggers.now
    assert list(initial_triggers) == list(sw.triggers)
