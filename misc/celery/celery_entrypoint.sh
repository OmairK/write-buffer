#!/bin/bash

cd scheduler
# Start Celery Beat
celery -A tasks beat info --beat &> /log/celery_beat.log&

# Start Celery Workers
celery -A tasks worker --loglevel=DEBUG
