# Spiel

[![PyPI](https://img.shields.io/pypi/v/spiel)](https://pypi.org/project/spiel)
[![PyPI - License](https://img.shields.io/pypi/l/spiel)](https://pypi.org/project/spiel)
[![Docs](https://img.shields.io/badge/docs-exist-brightgreen)](https://www.spiel.how)

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/JoshKarpel/spiel/main.svg)](https://results.pre-commit.ci/latest/github/JoshKarpel/spiel/main)
[![codecov](https://codecov.io/gh/JoshKarpel/spiel/branch/main/graph/badge.svg?token=2sjP4V0AfY)](https://codecov.io/gh/JoshKarpel/spiel)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![GitHub issues](https://img.shields.io/github/issues/JoshKarpel/spiel)](https://github.com/JoshKarpel/spiel/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/JoshKarpel/spiel)](https://github.com/JoshKarpel/spiel/pulls)

Spiel is a framework for building and presenting [richly-styled](https://github.com/Textualize/rich) presentations in your terminal using Python.

To see what Spiel can do without installing it, you can view the demonstration deck in a container:
```bash
$ docker run -it --rm ghcr.io/joshkarpel/spiel
```
Alternatively, install Spiel (`pip install spiel`) and run this command to view the demonstration deck:
```bash
$ spiel demo present
```

![The first slide of the demo deck](https://raw.githubusercontent.com/JoshKarpel/spiel/main/docs/assets/demo.svg)
![The demo deck in "deck view"](https://raw.githubusercontent.com/JoshKarpel/spiel/main/docs/assets/deck.svg)

## Quick Start

If you want to jump right in,
install Spiel (`pip install spiel`),
create a file called `deck.py`,
and copy this code into it:
```python
from rich.console import RenderableType

from spiel import Deck, present

deck = Deck(name="Your Deck Name")


@deck.slide(title="Slide 1 Title")
def slide_1() -> RenderableType:
    return "Your content here!"


if __name__ == "__main__":
    present(__file__)
```

That is the most basic Spiel presentation you can make.
To present the deck, run `python deck.py`.
You should see:

![Barebones slide](https://raw.githubusercontent.com/JoshKarpel/spiel/main/docs/assets/quickstart_basic.svg)

Check out the [Quick Start tutorial](https://www.spiel.how/quickstart) to continue!

## Documentation

To learn more about Spiel, take a look at the [documentation](https://www.spiel.how).
