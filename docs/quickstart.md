# Quick Start

After installing Spiel, create a file called `deck.py` and paste this code in:
```python
from spiel import Deck, present

deck = Deck(name="Your Deck Name")


@deck.slide(title="Slide 1 Title")
def slide1():
    return """Your content here!"""


if __name__ == "__main__":
    present(__file__)

```

That is the most basic Spiel presentation you can make. In the folder where you created `deck.py`, run `python deck.py`. You should see:

![Barebones slide](https://raw.githubusercontent.com/JoshKarpel/spiel/main/docs/assets/quickstart_basic.svg)

To recap, you first create a `Deck` that has the name of your presentation.

Then you create slide functions with the `@deck.slide()` decorator.

The slide function should return anything that [Rich can render](https://rich.readthedocs.io/en/stable/console.html#printing); that return value will be displayed as the slide in the presentation.

Finally, you call `present()` to run the presentation.

You can make your slides a lot prettier, of course.
As mentioned above, Spiel renders its slides using Rich, so you can bring in Rich functionality to spruce up your slides.
Let's explore some advanced features by recreating one of the slides from the demo deck.
Update your `deck.py` file with these imports and utility definitions:

``` python
import inspect
from textwrap import dedent

from rich.box import SQUARE
from rich.console import RenderableType
from rich.layout import Layout
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.style import Style
from rich.syntax import Syntax

from spiel import Deck, Slide, present
from spiel.deck import Deck


SPIEL = "[Spiel](https://github.com/JoshKarpel/spiel)"
RICH = "[Rich](https://rich.readthedocs.io/)"

def pad_markdown(markup: str) -> RenderableType:
    return Padding(Markdown(dedent(markup), justify="center"), pad=(0, 5))

```

And then paste this code in to your `deck.py` file below your first slide:

```python
@deck.slide(title="Decks and Slides")
def code() -> RenderableType:
    markup = f"""\
        ## Decks are made of Slides

        Here's the code for `Deck` and `Slide`!

        The source code is pulled directly from the definitions via [inspect.getsource](https://docs.python.org/3/library/inspect.html#inspect.getsource).

        ({RICH} supports syntax highlighting, so {SPIEL} does too!)
        """
    root = Layout()
    upper = Layout(pad_markdown(markup), size=len(markup.split("\n")) + 1)
    lower = Layout()
    root.split_column(upper, lower)

    def make_code_panel(obj: type) -> RenderableType:
        lines, line_number = inspect.getsourcelines(obj)
        return Panel(
            Syntax(
                "".join(lines),
                lexer="python",
                line_numbers=True,
                start_line=line_number,
            ),
            box=SQUARE,
            border_style=Style(dim=True),
            height=len(lines) + 2,
        )

    lower.split_row(
        Layout(make_code_panel(Deck)),
        Layout(make_code_panel(Slide)),
    )

    return root
```

And when you run the Python file:

![Demo Code Slide](https://raw.githubusercontent.com/JoshKarpel/spiel/main/docs/assets/quickstart_code.svg)

This uses Rich's Layout and Panel classes to create the layout and sytax highlighting.
Because Spiel runs entirely within Python, we can use the Python inspect library to dynamically reference source code and pretty print it via Rich's Syntax library.

Adding more slides is as easy as adding more functions with the `@deck.slide()` decorator.
The order of the functions in your file is the order in which they appear in your presentation.

Check out the source code of the [demo](https://github.com/JoshKarpel/spiel/blob/main/spiel/demo/demo.py) for more inspiration on ways to use Rich to make your slides beautiful! You can:
* View the demo in your terminal by running `spiel demo present`
* View the source in your terminal with `spiel demo source`
* Copy it to use as a starting point with `spiel demo copy <destination>`
