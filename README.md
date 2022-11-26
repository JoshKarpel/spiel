# Spiel

[![PyPI](https://img.shields.io/pypi/v/spiel)](https://pypi.org/project/spiel/)
[![Documentation Status](https://readthedocs.org/projects/spiel/badge/?version=latest)](https://spiel.readthedocs.io/en/latest/?badge=latest)
[![PyPI - License](https://img.shields.io/pypi/l/spiel)](https://pypi.org/project/spiel/)

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/JoshKarpel/spiel/main.svg)](https://results.pre-commit.ci/latest/github/JoshKarpel/spiel/main)
[![codecov](https://codecov.io/gh/JoshKarpel/spiel/branch/main/graph/badge.svg?token=2sjP4V0AfY)](https://codecov.io/gh/JoshKarpel/spiel)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![GitHub issues](https://img.shields.io/github/issues/JoshKarpel/spiel)](https://github.com/JoshKarpel/spiel/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/JoshKarpel/spiel)](https://github.com/JoshKarpel/spiel/pulls)

Spiel is a framework for building and presenting richly-styled presentations in your terminal using Python.

To see what Spiel can do without installing it, you can view the demonstration deck in a container:
```bash
$ docker run -it --rm ghcr.io/joshkarpel/spiel
```
Alternatively, install Spiel (`pip install spiel`) and run this command to view the demonstration deck:
```bash
$ spiel demo present
```

![The first slide of the demo deck](./assets/demo.svg)
![The demo deck in "deck view"](./assets/deck.svg)

## Sandboxed Execution via Containers

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
