FROM python:3.9

ENV COLORTERM=truecolor

RUN : \
 && apt-get update \
 && apt-get install -y vim \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && :

WORKDIR /app

COPY . /app/spiel
RUN : \
 && pip install --no-cache-dir /app/spiel \
 && spiel version \
 && :

CMD ["spiel", "demo", "present"]
