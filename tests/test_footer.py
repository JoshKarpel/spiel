from io import StringIO

from rich.console import Console

from spiel.footer import Footer
from spiel.rps import RPSCounter
from spiel.state import State


def test_deck_name_in_footer(console: Console, output: StringIO, three_slide_state: State) -> None:
    footer = Footer(state=three_slide_state, rps_counter=RPSCounter())

    console.print(footer)

    result = output.getvalue()
    print(repr(result))
    assert three_slide_state.deck.name in result
