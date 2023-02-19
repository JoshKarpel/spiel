from __future__ import annotations

from enum import Enum
from typing import Protocol, runtime_checkable

from textual.widget import Widget


class Direction(Enum):
    """
    An enumeration that describes which direction a slide transition
    animation should move in: whether we're going to the next slide,
    or to the previous slide.
    """

    Next = "next"
    """Indicates that the transition should handle going to the next slide."""

    Previous = "previous"
    """Indicates that the transition should handle going to the previous slide."""


@runtime_checkable
class Transition(Protocol):
    """
    A protocol that describes how to implement a transition animation.

    See [Writing Custom Transitions](./transitions.md#writing-custom-transitions)
    for more details on how to implement the protocol.
    """

    def initialize(
        self,
        from_widget: Widget,
        to_widget: Widget,
        direction: Direction,
    ) -> None:
        """
        A hook function to set up any CSS that should be present at the start of the transition.

        Args:
            from_widget: The widget showing the slide that we are leaving.
            to_widget: The widget showing the slide that we are entering.
            direction: The desired direction of the transition animation.
        """
        ...

    def progress(
        self,
        from_widget: Widget,
        to_widget: Widget,
        direction: Direction,
        progress: float,
    ) -> None:
        """
        A hook function that is called each time the `progress`
        of the transition animation updates.

        Args:
            from_widget: The widget showing the slide that we are leaving.
            to_widget: The widget showing the slide that we are entering.
            direction: The desired direction of the transition animation.
            progress: The progress of the animation, as a percentage
                (e.g., initial state is `0`, final state is `100`).
                Note that this is **not necessarily** bounded between `0` and `100`,
                nor is it necessarily [monotonically increasing](https://en.wikipedia.org/wiki/Monotonic_function),
                depending on the underlying Textual animation easing function,
                which may overshoot or bounce.
                However, it will always start at `0` and end at `100`,
                no matter which `direction` the transition should move in.
        """
        ...
