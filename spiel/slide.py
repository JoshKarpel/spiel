from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from typing import Callable, Mapping, Type

from rich.console import RenderableType
from rich.text import Text

from spiel.transition import Swipe, Transition
from spiel.triggers import Triggers

TRIGGERS = "triggers"

Content = Callable[..., RenderableType]


@dataclass
class Slide:
    """
    Represents a single slide in the presentation.
    """

    title: str = ""
    """The title of the `Slide`, which will be displayed in the footer."""

    content: Content = lambda: Text()
    """\
    A callable that is invoked by Spiel to display the slide's content.

    The function may optionally take arguments with these names:

    - `trigger`: The current [`Trigger`][spiel.Triggers] state, for use in animations.
    """

    bindings: Mapping[str, Callable[..., None]] = field(default_factory=dict)
    """\
    A mapping of
    [keys](https://textual.textualize.io/guide/input/#key)
    to callables to be executed when those keys are pressed,
    when on this slide.
    """

    transition: Type[Transition] | None = Swipe
    """\
    The transition animation to use when moving to this slide.
    Set to `None` to use the
    [`Deck.default_transition`][spiel.Deck.default_transition]
    of the deck this slide is in.
    """

    def render(self, triggers: Triggers) -> RenderableType:
        signature = inspect.signature(self.content)

        kwargs: dict[str, object] = {}
        if TRIGGERS in signature.parameters:
            kwargs[TRIGGERS] = triggers

        return self.content(**kwargs)
