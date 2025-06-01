import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'review_project.settings')

app = Celery('review_project',
             include=['reviews.tasks'])

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()