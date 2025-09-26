import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cts_backend.settings')

app = Celery('cts_backend')

app.conf.update(
  broker_url='redis://127.0.0.1:6379/0',
  result_backend='redis://127.0.0.1:6379/0',
  broker_connection_retry_on_startup=True,
  task_serializer='json',
  result_serializer='json',
  accept_content=['json'],
  timezone='America/Santiago',
  enable_utc=True,
)

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
  print(f'Request: {self.request!r}')