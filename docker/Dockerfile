FROM python:3.9

ENV COLORTERM=truecolor

WORKDIR /app

COPY . /app/spiel
RUN pip install --no-cache-dir /app/spiel

CMD ["spiel", "demo", "present"]
