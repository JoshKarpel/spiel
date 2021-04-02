from typing import Any, Iterable, Optional


def joinify(joiner: str, items: Iterable[Optional[Any]]) -> str:
    return joiner.join(map(str, filter(None, items)))


def clamp(value: int, lower: int, upper: int) -> int:
    if lower > upper:
        raise ValueError(
            f"Upper bound ({upper}) for clamp must be greater than lower bound ({lower})."
        )
    return max(min(value, upper), lower)
