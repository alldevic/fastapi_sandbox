ARG BASE_IMAGE

FROM ${BASE_IMAGE}

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/

COPY Pipfile Pipfile.lock /tmp/

RUN cd /tmp && pipenv requirements > requirements.txt \
    && pip install \
        --no-cache-dir \
        --no-binary pydantic \
        --no-compile \
        -r /tmp/requirements.txt \
    && python3 -m compileall -q -b /usr/local/lib/python*/dist-packages/* \
    && find /usr/local/lib/python*/dist-packages/* -name "*.py" | xargs rm -rf \
    && find /usr/local/lib/python*/dist-packages/* -name '*.c' -delete \
    && find /usr/local/lib/python*/dist-packages/* -name '*.pxd' -delete \
    && find /usr/local/lib/python*/dist-packages/* -name '*.pyd' -delete \
    && find /usr/local/lib/python*/dist-packages/* -name '__pycache__' | xargs rm -rf
