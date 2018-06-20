import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'translations.settings')

app = Celery('translations')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(packages=None)