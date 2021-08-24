FROM ghcr.io/cyb3r-jak3/pypy-flask:alpine

COPY requirements.txt /tmp/pip-tmp/
RUN pip --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

COPY app /usr/src/app/app

WORKDIR /usr/src/app

ENTRYPOINT ["gunicorn", "-k", "gevent","--preload", "--bind", "0.0.0.0", "--workers", "8", "app:app"]