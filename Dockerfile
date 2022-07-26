FROM python:3.10.5-alpine3.15

RUN apk add git; \
    pip install -r requirements.txt;
