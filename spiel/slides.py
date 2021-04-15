from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from functools import cached_property
from time import monotonic
from typing import Any, Callable, Dict, Iterator, List, Tuple, Union

from abc import ABC, abstractmethod
from rich.console import ConsoleRenderable
from rich.text import Text

MakeRenderable = Callable[..., ConsoleRenderable]
RenderableLike = Union[MakeRenderable, ConsoleRenderable]


@dataclass
class Presentable(ABC):
    title: str = ""

    @abstractmethod
    def render(self, trigger_times: List[float]) -> ConsoleRenderable:
        raise NotImplementedError


@dataclass(frozen=True)
class Triggers:
    times: Tuple[float, ...]
    now: float = field(default_factory=monotonic)

    def __len__(self) -> int:
        return len(self.times)

    def __getitem__(self, idx: int) -> float:
        return self.times[idx]

    def __iter__(self) -> Iterator[float]:
        return iter(self.times)

    @cached_property
    def time_since_last_trigger(self) -> float:
        return self.now - self.times[-1]

    @cached_property
    def time_since_first_trigger(self) -> float:
        return self.now - self.times[0]


@dataclass
class Slide(Presentable):
    content: RenderableLike = field(default_factory=Text)

    def render(self, trigger_times: List[float]) -> ConsoleRenderable:
        if callable(self.content):
            signature = inspect.signature(self.content)

            kwargs: Dict[str, Any] = {}
            if "triggers" in signature.parameters:
                kwargs["triggers"] = Triggers(times=tuple(trigger_times))

            return self.content(**kwargs)
        else:
            return self.content


@dataclass
class Deck:
    name: str
    slides: List[Presentable] = field(default_factory=list)

    def __getitem__(self, idx: int) -> Presentable:
        return self.slides[idx]

    def __len__(self) -> int:
        return len(self.slides)

    def __iter__(self) -> Iterator[Presentable]:
        yield from self.slides

    def add_slides(self, *slides: Presentable) -> Deck:
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
