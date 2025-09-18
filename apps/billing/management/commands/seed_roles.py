from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.billing.models import Plan, Customer, Subscription, Invoice, InvoiceItem, Payment

ROLE_PERMS = {
    "Admin": {"all": True},
    "Finance": {
        "models": [Plan, Customer, Subscription, Invoice, InvoiceItem, Payment],
        "perms": ["add", "change", "delete", "view"],
    },
    "Support": {
        "models": [Customer, Subscription, Invoice, Payment],
        "perms": ["view"],
    },
    "Developer": {
        "models": [Plan],
        "perms": ["view"],
    },
    "Customer": {
        "models": [Customer, Subscription, Invoice],
        "perms": ["view"],
    },
}

class Command(BaseCommand):
    help = "Create default groups and attach model permissions"

    def handle(self, *args, **options):
        for role, cfg in ROLE_PERMS.items():
            group, _ = Group.objects.get_or_create(name=role)
            if cfg.get("all"):
                perms = Permission.objects.all()
            else:
                perms = []
                for model in cfg["models"]:
                    ct = ContentType.objects.get_for_model(model)
                    for p in cfg["perms"]:
                        codename = f"{p}_{model._meta.model_name}"
                        try:
                            perms.append(Permission.objects.get(content_type=ct, codename=codename))
                        except Permission.DoesNotExist:
                            self.stdout.write(self.style.WARNING(f"Permission missing: {codename}"))
            group.permissions.set(perms)
            group.save()
            self.stdout.write(self.style.SUCCESS(f"Seeded role: {role} with {len(perms)} permissions"))
        self.stdout.write(self.style.SUCCESS("Done"))
