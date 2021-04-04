from rich.console import Console

from spiel.help import Help
from spiel.state import State


def test_can_render_help(console: Console, three_slide_state: State) -> None:
    console.print(Help(three_slide_state))
