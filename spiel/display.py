import sys

from rich.console import Console
from rich.layout import Layout
from rich.live import Live

from .footer import Footer
from .input import handle_input, no_echo
from .modes import Mode
from .state import State


def display_deck(console: Console, state: State) -> None:
    def get_renderable() -> Layout:
        footer = Layout(Footer(state), name="footer", size=1)

        current_slide = state.deck[state.current_slide_idx]

        if state.mode is Mode.SLIDE:
            content = current_slide.content
        else:
            raise

        body = Layout(content, name="body", ratio=1)

        root = Layout(name="root")
        root.split_column(body, footer)

        return root

    with no_echo(), Live(
        get_renderable=get_renderable,
        console=console,
        screen=True,
        auto_refresh=True,
        refresh_per_second=4,
        vertical_overflow="visible",
    ) as live:
        try:
            while True:
                get_renderable()
                handle_input(state, sys.stdin)
        except Exception:
            live.stop()
            console.print_exception(show_locals=True)
