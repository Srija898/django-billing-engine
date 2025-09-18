from django.apps import AppConfig
from django.contrib.auth import get_user_model
import os

class BillingEngineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'billing_engine'

    def ready(self):
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="Srija123",
                email="srijamorthala104@gmail.com",
                password="django123"
            )