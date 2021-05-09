from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Options:
    profiling: bool = False
