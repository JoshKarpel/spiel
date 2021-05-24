#!/usr/bin/env python

import os

from rich.console import Console

from spiel.main import DEMO_SOURCE
from spiel.present import render_slide
from spiel.state import State

CYCLES_PER_SLIDE = 10
TRIGGERS_PER_SLIDE = 10


def render_demo_repeatedly() -> None:
    with open(os.devnull, "w") as f:
        state = State.from_file(DEMO_SOURCE, console=Console(file=f))

        for _ in range(CYCLES_PER_SLIDE):
            for slide in state.deck:
                for _ in range(TRIGGERS_PER_SLIDE):
                    rendered = render_slide(state, slide)
                    state.console.print(rendered)
                    state.trigger()
                state.reset_trigger()


if __name__ == "__main__":
    render_demo_repeatedly()
