from spiel import Triggers
from spiel.demo.demo import DemoRenderFailure, deck


def test_can_render_every_demo_slide() -> None:
    for slide in deck:
        try:
            slide.render(triggers=Triggers.new())
        except DemoRenderFailure:
            pass
