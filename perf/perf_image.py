#!/usr/bin/env python

import os

from rich.console import Console

from spiel.main import DEMO_SOURCE
from spiel.present import render_slide
from spiel.state import State

CYCLES_PER_SLIDE = 100


def render_image_repeatedly() -> None:
    with open(os.devnull, "w") as f:
        state = State.from_file(DEMO_SOURCE, console=Console(file=f))

        for _ in range(CYCLES_PER_SLIDE):
            slide = [slide for slide in state.deck.slides if "Image" in slide.title][0]
            rendered = render_slide(state, slide)
            state.console.print(rendered)


if __name__ == "__main__":
    render_image_repeatedly()
