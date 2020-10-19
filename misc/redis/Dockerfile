FROM redis:alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN mkdir /redis

WORKDIR /redis

COPY . /redis/

CMD [ "redis-server", "--loglevel", "verbose"]
