FROM python:3.8.5-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV POSTGRES_DB="locale_task"
ENV POSTGRES_USER="locale_test"
ENV POSTGRES_PASSWORD="locale-test"
ENV POSTGRES_HOST="db"
ENV POSTGRES_PORT 5432
ENV CELERY_BROKER_URL="redis://redis:6379"
ENV CELERY_RESULT_BACKEND="redis://redis:6379"
ENV REDIS_HOST="redis"
ENV REDIS_PORT 6379

RUN apk update \
	&& apk add postgresql-dev gcc python3-dev musl-dev
RUN apk update && apk add bash
RUN mkdir /celery

RUN mkdir /log
RUN touch /log/celery.log && touch /log/celery_beat.log
WORKDIR /celery


COPY celery_requirement.txt /celery/
RUN pip install -r celery_requirement.txt

COPY . /celery/
RUN chmod a+x /celery/celery_entrypoint.sh


CMD [ "./celery_entrypoint.sh" ]
