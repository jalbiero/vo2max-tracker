FROM python:3.11.1-alpine3.17

COPY ./dist/*.tar.gz /tmp/vo2max-tracker/

WORKDIR /tmp/vo2max-tracker

RUN apk add --no-cache --virtual .build-deps musl-dev linux-headers g++ gcc zlib-dev make python3-dev jpeg-dev

RUN pip install vo2max_tracker-0.1.0.tar.gz 