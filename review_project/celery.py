import os
from celery import Celery

# Ustaw domyślny moduł Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'review_project.settings')

# Utwórz instancję Celery
app = Celery('review_project',
             include=['reviews.tasks'])

# Wczytaj konfigurację z settings.py (prefix "CELERY_")
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatycznie wykryj zadania z wszystkich aplikacji Django
app.autodiscover_tasks()