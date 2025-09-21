from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError, ProgrammingError

class BillingConfig(AppConfig):  # Match INSTALLED_APPS
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.billing"  # MUST match your folder structure

    def ready(self):
        User = get_user_model()
        try:
            if not User.objects.filter(username="Srija123").exists():
                User.objects.create_superuser(
                    username="srija123",
                    email="srijamorthala104@gmail.com",
                    password="django123"
                )
        except (OperationalError, ProgrammingError):
            pass
