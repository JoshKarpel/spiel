import sys
from itertools import islice
from math import ceil
from time import monotonic

from rich.console import ConsoleRenderable
from rich.layout import Layout
from rich.live import Live
from rich.padding import Padding
from rich.panel import Panel
from rich.style import Style

from spiel.constants import TARGET_RPS
from spiel.exceptions import UnknownModeError
from spiel.footer import Footer
from spiel.help import Help
from spiel.input import handle_input, no_echo
from spiel.modes import Mode
from spiel.presentable import Presentable
from spiel.rps import RPSCounter
from spiel.state import State
from spiel.triggers import Triggers
from spiel.utils import clamp, filter_join


def render_slide(state: State, slide: Presentable) -> ConsoleRenderable:
    return Padding(
        slide.render(triggers=Triggers(times=tuple(state.trigger_times))),
        pad=1,
    )


def split_layout_into_deck_grid(root: Layout, state: State) -> Layout:
    grid_width = state.deck_grid_width
    row_of_current_slide = state.current_slide_idx // grid_width
    num_rows = ceil(len(state.deck) / grid_width)
    start_row = clamp(
        value=row_of_current_slide - (grid_width // 2),
        lower=0,
        upper=max(num_rows - grid_width, 0),
    )
    start_slide_idx = grid_width * start_row
    slides = islice(enumerate(state.deck.slides, start=1), start_slide_idx, None)

    rows = [Layout(name=str(r)) for r in range(grid_width)]
    cols = [[Layout(name=f"{r}-{c}") for c in range(grid_width)] for r, _ in enumerate(rows)]

    root.split_column(*rows)
    for row, layouts in zip(rows, cols):
        for layout in layouts:
            slide_number, slide = next(slides, (None, None))
            if slide is None:
                layout.update("")
            else:
                is_active_slide = slide is state.current_slide
                layout.update(
                    Panel(
                        slide.render(triggers=Triggers(times=(monotonic(),))),
                        title=filter_join(" | ", [slide_number, slide.title]),
                        border_style=Style(
                            color="bright_cyan" if is_active_slide else None,
                            dim=not is_active_slide,
                        ),
                    )
                )
        row.split_row(*layouts)

    return root


def present_deck(state: State) -> None:
    rps_counter = RPSCounter()
    footer = Layout(Footer(state, rps_counter), name="footer", size=1)
    help = Layout(Help(state), name="help")

    def get_renderable() -> Layout:
        current_slide = state.deck[state.current_slide_idx]

        body = Layout(name="body", ratio=1)
        if state.mode is Mode.SLIDE:
            body.update(render_slide(state, current_slide))
        elif state.mode is Mode.DECK:
            split_layout_into_deck_grid(body, state)
        elif state.mode is Mode.HELP:
            body.update(help)
        elif state.mode is Mode.OPTIONS:
            body.update(state.options)
        else:  # pragma: unreachable
            raise UnknownModeError(f"Unrecognized mode: {state.mode!r}")

        root = Layout(name="root")
        root.split_column(body, footer)

        rps_counter.mark()

        return root

    with no_echo(), Live(
        get_renderable=get_renderable,
        console=state.console,
        screen=True,
        auto_refresh=True,
        refresh_per_second=TARGET_RPS,
        vertical_overflow="visible",
    ) as live:
        while True:
            handle_input(state, sys.stdin)
            live.refresh()
