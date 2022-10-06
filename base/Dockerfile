ARG DIST=jammy

FROM ubuntu:${DIST} AS base

ARG DIST
ARG ARCH=amd64
# ENV ARCH='dpkg --print-architecture'
ARG UNIT_VERSION=1.28.0-1
ARG PY3_VERSION=3.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV REPO=https://packages.nginx.org/unit/ubuntu/pool/unit/u
ENV UNIT_PKG=unit_${UNIT_VERSION}~${DIST}_${ARCH}.deb
ENV UNIT_PY3_PKG=unit-python${PY3_VERSION}_${UNIT_VERSION}~${DIST}_${ARCH}.deb

RUN apt-get update && apt-get install -y --no-install-recommends --no-install-suggests --no-upgrade \
        curl \
        ca-certificates \
        python${PY3_VERSION} \
        python3-pip \
        python-is-python3 \
    && curl -O ${REPO}/unit/${UNIT_PKG} \
    && curl -O ${REPO}/unit-python${PY3_VERSION}/${UNIT_PY3_PKG} \
    && apt-get install -y \
        ./${UNIT_PKG} \
        ./${UNIT_PY3_PKG} \
    && apt-get clean \
    && rm -rf ./${UNIT_PKG} ./${UNIT_PY3_PKG} /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list \
    && ln -sf /dev/stdout /var/log/unit.log \
    && mkdir /docker-entrypoint.d/ \
    && userdel unit \ 
    && addgroup --system unit \
    && adduser \
        --system \
        --disabled-login \
        --ingroup unit \
        --no-create-home \
        --home /nonexistent \
        --gecos "unit user" \
        --shell /bin/false \
        unit \
    && unitd --version

STOPSIGNAL SIGTERM

COPY docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

CMD ["unitd", "--no-daemon", "--control", "unix:/var/run/control.unit.sock"]
