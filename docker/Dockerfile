FROM python:3.9

RUN : \
 && apt-get update \
 && apt-get install -y vim emacs nano \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && :

ENV COLORTERM=truecolor \
    EDITOR=/usr/bin/vim

WORKDIR /app

COPY . /app/spiel
RUN : \
 && pip install --no-cache-dir /app/spiel \
 && spiel version \
 && :

CMD ["spiel", "demo", "present"]
