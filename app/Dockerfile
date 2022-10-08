ARG BASE_IMAGE

FROM ${BASE_IMAGE}

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/

COPY Pipfile Pipfile.lock /tmp/

RUN cd /tmp && pipenv requirements > requirements.txt \
    && pip install --no-cache-dir --no-compile -r /tmp/requirements.txt \
    && rm -rf /tmp/*
