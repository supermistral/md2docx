FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN apk add git

COPY ./reqs/main.txt .

RUN apk add --no-cache pandoc && \
    # https://github.com/yaml/pyyaml/issues/724
    pip install "cython<3.0.0" && \
    pip install --no-build-isolation pyyaml==6.0 && \
    pip install --no-cache-dir -r main.txt && \
    # https://github.com/IndominusByte/fastapi-jwt-auth/issues/98
    pip install git+https://github.com/vvpreo/fastapi-jwt-auth.git#egg=fastapi-jwt-auth