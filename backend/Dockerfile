FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY ./reqs/main.txt .

RUN apk add --no-cache pandoc && \
    pip install --no-cache-dir -r main.txt