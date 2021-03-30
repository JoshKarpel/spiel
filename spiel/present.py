import sys
from itertools import islice

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.style import Style

from .exceptions import UnknownModeError
from .footer import Footer
from .input import handle_input, no_echo
from .modes import Mode
from .state import State
from .utils import joinify


def present_deck(console: Console, state: State) -> None:
    def get_renderable() -> Layout:
        footer = Layout(Footer(state), name="footer", size=1)

        current_slide = state.deck[state.current_slide_idx]

        body = Layout(name="body", ratio=1)
        if state.mode is Mode.SLIDE:
            body.update(current_slide.content)
        elif state.mode is Mode.DECK:
            n = console.size.width // 30
            row_of_current_slide = state.current_slide_idx // n
            slides = islice(
                enumerate(state.deck.slides, start=1),
                n * max(0, row_of_current_slide - (n // 2)) if n ** 2 < len(state.deck) else 0,
                None,
            )

            rows = [Layout(name=str(r)) for r in range(n)]
            cols = [[Layout(name=f"{r}-{c}") for c in range(n)] for r, _ in enumerate(rows)]

            body.split_column(*rows)
            for row, layouts in zip(rows, cols):
                for layout in layouts:
                    slide_idx, slide = next(slides, (None, None))
                    if slide is None:
                        layout.update("")
                    else:
                        is_active_slide = slide is state.current_slide
                        layout.update(
                            Panel(
                                slide.content,
                                title=joinify(" | ", [slide_idx, slide.title]),
                                border_style=Style(
                                    color="bright_cyan" if is_active_slide else None,
                                    dim=not is_active_slide,
                                ),
                            )
                        )
                row.split_row(*layouts)
        else:
            raise UnknownModeError(f"Unrecognized mode: {state.mode!r}")

        root = Layout(name="root")
        root.split_column(body, footer)

        return root

    with no_echo(), Live(
        get_renderable=get_renderable,
        console=console,
        screen=True,
        auto_refresh=True,
        refresh_per_second=10,
        vertical_overflow="visible",
    ) as live:
        try:
            while True:
                handle_input(state, sys.stdin)
                live.refresh()
        except Exception:
            live.stop()
            console.print_exception(show_locals=True)
