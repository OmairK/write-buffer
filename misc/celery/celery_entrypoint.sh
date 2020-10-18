#!/bin/bash

# Start Celery Workers
celery worker --workdir /app --app dri -l info &> /log/celery.log  &

# Start Celery Beat
celery -A tasks beat info --beat &> /log/celery_beat.log  &
