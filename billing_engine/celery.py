import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "billing_engine.settings")
app = Celery("billing_engine")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
