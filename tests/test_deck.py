from spiel.slides import Slide, Deck


def test_can_add_slide_to_deck(three_slide_deck: Deck) -> None:
    initial_len = len(three_slide_deck)
    new_slide = Slide()

    three_slide_deck.add_slide(new_slide)

    assert len(three_slide_deck) == initial_len + 1
    assert three_slide_deck[-1] is new_slide
