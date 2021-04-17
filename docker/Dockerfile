FROM python:3.9

RUN : \
 && apt-get update \
 && apt-get install -y vim emacs nano \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && :

WORKDIR /app

COPY . /app/spiel
RUN : \
 && pip install --no-cache-dir /app/spiel ipython \
 && spiel version \
 && :

ENV COLORTERM=truecolor \
    EDITOR=/usr/bin/vim

CMD ["spiel", "demo", "present"]
