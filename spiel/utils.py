from typing import Any, Iterable, Optional


def joinify(joiner: str, items: Iterable[Optional[Any]]) -> str:
    return joiner.join(map(str, filter(None, items)))
