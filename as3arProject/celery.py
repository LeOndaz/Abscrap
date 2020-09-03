import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'as3arProject.settings')

app = Celery('as3arProject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
