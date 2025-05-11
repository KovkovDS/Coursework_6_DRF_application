import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Coursework_6_DRF.settings")

app = Celery("Coursework_6_DRF")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
