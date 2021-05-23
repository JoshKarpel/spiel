from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Any, Mapping

import toml
from rich.align import Align
from rich.console import ConsoleRenderable
from rich.padding import Padding
from rich.table import Column, Table

from .constants import PACKAGE_NAME
from .exceptions import InvalidOptionValue
from .notebooks import NOTEBOOKS
from .repls import REPLS


@dataclass
class Options:
    repl: str = "ipython"
    notebook: str = "nbterm"
    footer_time_format: str = "YYYY-MM-DD hh:mm A"
    profiling: bool = True

    def __post_init__(self) -> None:
        if self.repl not in REPLS:
            raise InvalidOptionValue(f"repl must be one of: {set(REPLS.keys())}")

        if self.notebook not in NOTEBOOKS:
            raise InvalidOptionValue(f"notebook must be one of: {set(NOTEBOOKS.keys())}")

    def as_dict(self) -> Mapping[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "Options":
        fields_by_name = {field.name: field for field in fields(cls)}
        only_valid = {k: fields_by_name[k].type(v) for k, v in d.items() if k in fields_by_name}
        return cls(**only_valid)

    def as_toml(self) -> str:
        return toml.dumps({PACKAGE_NAME: self.as_dict()})

    @classmethod
    def from_toml(cls, t: str) -> "Options":
        return cls.from_dict(toml.loads(t).get(PACKAGE_NAME, {}))

    def save(self, path: Path) -> Path:
        path.write_text(self.as_toml())
        return path

    @classmethod
    def load(cls, path: Path) -> "Options":
        return cls.from_toml(path.read_text())

    def __rich__(self) -> ConsoleRenderable:
        table = Table(
            Column("Option"),
            Column("Type", justify="center"),
            Column("Value"),
            show_lines=True,
        )

        fields_by_name = {field.name: field for field in fields(self)}

        for key, value in self.as_dict().items():
            table.add_row(key, fields_by_name[key].type.__name__, str(value))

        return Padding(
            Align.center(table),
            pad=(0, 1),
        )
