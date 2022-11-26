from spiel import Slide, Triggers


def test_can_render_default_slide() -> None:
    Slide().render(triggers=Triggers.new())
