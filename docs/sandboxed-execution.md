# Sandboxed Execution

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
