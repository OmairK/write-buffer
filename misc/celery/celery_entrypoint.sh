#!/bin/bash

cd scheduler
# Start Celery Beat
celery -A tasks beat --loglevel=DEBUG &> /log/celery_beat.log&

# Start Celery Workers
celery -A tasks worker --loglevel=DEBUG
