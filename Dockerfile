# syntax=docker/dockerfile:1

# base image
FROM python:3.11-alpine as python-base

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.6.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    VIRTUAL_ENV="/venv"

ENV PATH="${POETRY_HOME}/bin:${VIRTUAL_ENV}/bin:${PATH}"

RUN python -m venv ${VIRTUAL_ENV}

WORKDIR /app
ENV PYTHONPATH="/app:${PYTHONPATH}"

# builder image
FROM python-base as builder-base
RUN apk update && \
    apk upgrade && \
    apk add curl

RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python -

WORKDIR /app
COPY poetry.lock pyproject.toml ./
COPY emojibot/ emojibot/

RUN --mount=type=cache,target=/root/.cache \
    poetry install --no-root --only main

# development image
FROM builder-base as development-env

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache \
    poetry install --no-root --with dev

# production image
FROM builder-base as production-env

COPY --from=builder-base ${POETRY_HOME} ${POETRY_HOME}
COPY --from=builder-base ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /app
COPY poetry.lock pyproject.toml ./
COPY emojibot/ emojibot/