FROM python:3.8.5-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV DB_HOST="db"
ENV REDIS_HOST="redis"

RUN apk update \
	&& apk add postgresql-dev gcc python3-dev musl-dev
RUN apk update && apk add bash
RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/
