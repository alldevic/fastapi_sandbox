ARG BASE_IMAGE

FROM ${BASE_IMAGE}

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/

COPY Pipfile Pipfile.lock /app/
ENV PYTHONPATH=/usr/bin/python
RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests --no-upgrade  python3-pip \
    && pip install pipenv \
    && pipenv install --system --deploy --ignore-pipfile \
    && pip uninstall pipenv virtualenv virtualenv-clone -y \
    && apt remove -y python3-pip \
    && apt autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list /root/.cache /root/.local
