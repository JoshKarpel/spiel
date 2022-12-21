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
#!/usr/bin/env python

from spiel import Deck, present

deck = Deck(...)

...  # construct your deck

if __name__ == "__main__":
    present(__file__)
```

You can then present the deck by running the script:
```console
$ python talk/slides.py
```
Or by running the script as a module (you must have a `talk/__init__.py` file):
```console
$ python -m talk.slides
```
Or by running the script via its [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix))
(after running `chmod +x talk/slides.py` to mark `talk/slides.py` as executable):
```console
$ talk/slides.py
```
