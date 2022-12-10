# Presenting Decks

Depending on your preferred workflow,
you can start a presentation in a variety of different ways.

## Using the `spiel` CLI

!!! warning "Under Construction"

## Using the `present` function

The `present` function lets you start a presentation programmatically (i.e., from a Python script).

::: spiel.present

If your deck is defined in `talk/slides.py` like so:

```python title="talk/slides.py"
from spiel import Deck, present

deck = Deck(name=f"pytest")

...  # construct your deck

if __name__ == "__main__":
    present(__file__)
```

You can then present the deck by running
```console
$ python talk/slides.py
```
or
```console
$ python -m talk.slides
```
