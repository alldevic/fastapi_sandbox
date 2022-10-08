FROM ubuntu:jammy AS base

ARG DIST
ARG UNIT_VERSION=1.28.0

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHON_PIP_VERSION 22.2.2
ENV PYTHON_SETUPTOOLS_VERSION 63.2.0
ENV PYTHON_GET_PIP_URL https://bootstrap.pypa.io/get-pip.py

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends --no-install-suggests --no-upgrade \
                build-essential \
                python3.10-dev \
                curl \
	&& cd /tmp \
	&& curl -O "http://unit.nginx.org/download/unit-$UNIT_VERSION.tar.gz" \
	&& tar xzf unit-$UNIT_VERSION.tar.gz \
	&& cd unit-$UNIT_VERSION \
	&& ./configure  --no-ipv6  --no-regex --control='*:8081' --prefix=/usr --modules=lib --log=/dev/stdout --pid=/var/run/unitd.pid \
	&& ./configure python --module=py310 --config=python3.10-config \
	&& make install \
	&& rm -rf /tmp/unit-$UNIT_VERSION* \
	&& apt-get purge --auto-remove -y  build-essential python3.10-dev \
	&& apt-get install -y --no-install-recommends --no-install-suggests --no-upgrade libpython3.10 python3.10 ca-certificates \
	&& rm -rf /var/lib/apt/lists/* \
	&& ln -s /usr/bin/python3.10 /usr/bin/python3 \
	&& ln -s /usr/bin/python3.10 /usr/bin/python \
	&& find /usr/lib/python*/* -name '__pycache__' | xargs rm -r \
	&& cd /app/ \
	&& curl -sSL $PYTHON_GET_PIP_URL -o get-pip.py  \
    && python get-pip.py --no-cache-dir --no-compile \
		"pip==$PYTHON_PIP_VERSION" \
		"setuptools==$PYTHON_SETUPTOOLS_VERSION" \
	&& rm -f get-pip.py \
	&& pip install --no-cache-dir --no-compile pipenv \
	&& unitd --version \
	&& python --version \
	&& pip --version \
	&& pipenv --version

COPY docker-entrypoint.sh /usr/local/bin/

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

CMD ["unitd", "--no-daemon"]
