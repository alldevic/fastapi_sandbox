ARG PROJECT_NAME

FROM ${PROJECT_NAME}_base:latest

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/

COPY Pipfile Pipfile.lock /app/

RUN pip install --disable-pip-version-check --no-cache-dir --ignore-installed pipenv \
    &&  pipenv install --system --deploy --ignore-pipfile \
    && pip uninstall pipenv virtualenv virtualenv-clone -y \
    && rm -rf /root/.cache /root/.local
