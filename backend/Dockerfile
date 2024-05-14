FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY ./reqs/main.txt .

RUN apk add --no-cache pandoc && \
    # https://github.com/yaml/pyyaml/issues/724
    pip install "cython<3.0.0" && \
    pip install --no-build-isolation pyyaml==6.0 && \
    pip install --no-cache-dir -r main.txt