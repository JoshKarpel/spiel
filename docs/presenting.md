# Presenting Decks

Depending on your preferred workflow,
you can start a presentation in a variety of different ways.

!!! danger "Sandboxed Execution"

    Spiel presentations are live Python code: they can do anything that Python can do.
    You may want to run untrusted presentations (or even your own presentations) inside a container (but remember, even containers are not perfectly safe!).
    We produce a [container image](https://github.com/users/JoshKarpel/packages/container/package/spiel)
    that can be run by (for example) Docker.

    Presentations without extra Python dependencies might just need to be bind-mounted into the container.
    For example, if your demo file is at `$PWD/presentation/deck.py`, you could do
    ```bash
    $ docker run -it --rm --mount type=bind,source=$PWD/presentation,target=/presentation ghcr.io/joshkarpel/spiel spiel present /presentation/deck.py
    ```

    If the presentation has extra dependencies (like other Python packages),
    we recommend building a new image that inherits our image (e.g., `FROM ghcr.io/joshkarpel/spiel:vX.Y.Z`).
    Spiel's image itself inherits from the [Python base image](https://hub.docker.com/_/python).


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
