from pathlib import Path

import typer
from rich.console import Console
from rich.text import Text

app = typer.Typer()
console = Console()


@app.command()
def display(path: Path) -> None:
    console.print(Text(str(path), justify="center"))
