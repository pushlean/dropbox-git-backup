# syntax=docker/dockerfile:1
FROM python:3.10.5-alpine3.15 as base

WORKDIR /app

COPY src requirements.txt /app/
ENV PYTHONPATH /app/src/

RUN apk add git; \
  pip install -U pip ; \
  pip install -r /app/requirements.txt;

FROM base as test
COPY tests /app/
RUN pip install pytest;
CMD ["pytest"]
