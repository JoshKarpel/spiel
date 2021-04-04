from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from time import monotonic
from typing import Any, Callable, Dict, Iterator, List, Union

from rich.console import ConsoleRenderable
from rich.text import Text

MakeRenderable = Callable[..., ConsoleRenderable]
RenderableLike = Union[MakeRenderable, ConsoleRenderable]


@dataclass
class Slide:
    content: RenderableLike = field(default_factory=Text)
    title: str = ""

    def render(self, trigger_times: List[float]) -> ConsoleRenderable:
        if callable(self.content):
            signature = inspect.signature(self.content)

            now = monotonic()

            kwargs: Dict[str, Any] = {}
            if "trigger_times" in signature.parameters:
                kwargs["trigger_times"] = trigger_times
            if "now" in signature.parameters:
                kwargs["now"] = now
            if "time_since_last_trigger" in signature.parameters:
                kwargs["time_since_last_trigger"] = now - trigger_times[-1]
            if "time_since_first_trigger" in signature.parameters:
                kwargs["time_since_last_trigger"] = now - trigger_times[0]

            return self.content(**kwargs)
        else:
            return self.content


@dataclass
class Deck:
    name: str
    slides: List[Slide] = field(default_factory=list)

    def __getitem__(self, idx: int) -> Slide:
        return self.slides[idx]

    def __len__(self) -> int:
        return len(self.slides)

    def __iter__(self) -> Iterator[Slide]:
        yield from self.slides

    def add_slides(self, *slides: Slide) -> Deck:
        self.slides.extend(slides)
        return self

    def slide(
        self,
        title: str = "",
    ) -> Callable[[MakeRenderable], MakeRenderable]:
        def slideify(content: MakeRenderable) -> MakeRenderable:
            slide = Slide(content=content, title=title)
            self.add_slides(slide)
            return content

        return slideify
