import pytest
from PIL import Image as Img
from rich.console import Console

from spiel.constants import DEMO_DIR
from spiel.renderables.image import Image, ImageSize


@pytest.fixture()
def image() -> Image:
    return Image(Img.new(mode="RGB", size=ImageSize(100, 100)))


@pytest.mark.parametrize(
    ("max_width", "height", "size"),
    [
        (100, None, ImageSize(100, 100)),
        (100, 50, ImageSize(100, 100)),
        (100, 25, ImageSize(50, 50)),
        (50, 25, ImageSize(50, 50)),
        (50, 50, ImageSize(50, 50)),
        (50, 100, ImageSize(50, 50)),
        (50, 10, ImageSize(20, 20)),
    ],
)
def test_determine_size(
    console: Console, image: Image, max_width: int, height: int, size: ImageSize
) -> None:
    options = console.options.update(max_width=max_width, height=height)

    assert image._determine_size(options) == size


def test_render_image(image: Image, console: Console) -> None:
    console.print(image)


def test_render_image_from_file(console: Console) -> None:
    image = Image.from_file(DEMO_DIR / "tree.jpg")

    console.print(image)
