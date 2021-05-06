FROM python:3.9-slim

# Don't periodically check PyPI to determine whether a new version of pip is available for download.
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
# Disable package cache.
ENV PIP_NO_CACHE_DIR=off
# Python won’t try to write .pyc files on the import of source modules.
ENV PYTHONDONTWRITEBYTECODE=on
# install a handler for SIGSEGV, SIGFPE, SIGABRT, SIGBUS and SIGILL signals to dump the Python traceback
ENV PYTHONFAULTHANDLER=on
# Force the stdout and stderr streams to be unbuffered.
ENV PYTHONUNBUFFERED=on
# set workdir as PYTHONPATH
ENV PYTHONPATH=/opt/app

ENV POETRY_VERSION=1.1.5
ARG ENVIRONMENT=production

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get autoclean && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*  \
    && pip install "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.create false

WORKDIR /opt/app

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN poetry install $(if test "$ENVIRONMENT" = production; then echo "--no-dev"; fi)

COPY app app
COPY Makefile Makefile

ENTRYPOINT []
