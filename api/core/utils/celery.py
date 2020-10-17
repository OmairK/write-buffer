from celery import Celery

app = Celery('write_buffer', broker='redis://localhost:6379/0')

@app.task
def f