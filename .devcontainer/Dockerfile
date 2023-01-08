ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}

RUN : \
 && apt-get update \
 && apt-get install -y vim emacs nano git less which  \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && python -m pip install pipx \
 && pipx install poetry \
 && :

ENV COLORTERM=truecolor \
    EDITOR=/usr/bin/vim
