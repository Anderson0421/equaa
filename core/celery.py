import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.conf.broker_url = os.getenv('CELERY_BROKER_URL')

app.autodiscover_tasks()
