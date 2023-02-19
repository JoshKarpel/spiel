from __future__ import annotations

from textual.widget import Widget

from spiel.transitions.protocol import Direction, Transition


class Swipe(Transition):
    """
    A transition where the current and incoming slide are placed side-by-side
    and gradually slide across the screen,
    with the current slide leaving and the incoming slide entering.
    """

    def initialize(
        self,
        from_widget: Widget,
        to_widget: Widget,
        direction: Direction,
    ) -> None:
        to_widget.styles.offset = ("100%" if direction is Direction.Next else "-100%", 0)

    def progress(
        self,
        from_widget: Widget,
        to_widget: Widget,
        direction: Direction,
        progress: float,
    ) -> None:
        match direction:
            case Direction.Next:
                from_widget.styles.offset = (f"-{progress:.2f}%", 0)
                to_widget.styles.offset = (f"{100 - progress:.2f}%", 0)
            case Direction.Previous:
                from_widget.styles.offset = (f"{progress:.2f}%", 0)
                to_widget.styles.offset = (f"-{100 - progress:.2f}%", 0)
