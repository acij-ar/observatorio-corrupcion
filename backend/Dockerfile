FROM python:3.8-buster

WORKDIR /app

# Setup poetry
RUN curl -o /tmp/install-poetry.py https://install.python-poetry.org \ 
# /https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py \
  && python /tmp/install-poetry.py --version 1.1.8 \
  && /root/.local/bin/poetry config virtualenvs.create false

ENV PATH="/root/.local/bin:${PATH}"

COPY pyproject.toml poetry.lock /app/
RUN poetry install
