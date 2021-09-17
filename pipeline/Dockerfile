FROM python:3.9-buster

WORKDIR /app

RUN apt update && apt install poppler-utils -y

# Setup poetry
RUN curl -o /tmp/install-poetry.py https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py \
  && python /tmp/install-poetry.py --version 1.1.8 \
  && /root/.local/bin/poetry config virtualenvs.create false

ENV PATH="/root/.local/bin:${PATH}"

COPY pyproject.toml poetry.lock /app/
RUN poetry install
