FROM python:3.10

RUN : \
 && apt-get update \
 && apt-get install -y vim emacs nano \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && :

ENV COLORTERM=truecolor \
    EDITOR=/usr/bin/vim

RUN --mount=target=/spiel : \
 && pip install --no-cache-dir --disable-pip-version-check /spiel \
 && spiel version \
 && :

WORKDIR /app

CMD ["spiel", "demo", "present"]
