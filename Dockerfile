FROM python:3.7.7-alpine3.11
MAINTAINER https://github.com/strpc

COPY requirements.txt /app/

RUN apk update \
    && apk add gcc \
    && apk add --no-cache python3 postgresql-libs \
    && apk add --update --no-cache --virtual .build-deps alpine-sdk python3-dev musl-dev postgresql-dev libffi-dev
RUN pip install wheel \
    && pip install -U setuptools pip \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && apk --purge del .build-deps
COPY . /app

WORKDIR /app