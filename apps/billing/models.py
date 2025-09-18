from django.conf import settings
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Plan(models.Model):
    name = models.CharField(max_length=120, unique=True)
    price_cents = models.PositiveIntegerField()
    currency = models.CharField(max_length=10, default="USD")
    interval = models.CharField(max_length=20, choices=[("month", "Month"), ("year", "Year")], default="month")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.price_cents/100:.2f} {self.currency}/{self.interval})"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
    company_name = models.CharField(max_length=200, blank=True)
    default_currency = models.CharField(max_length=10, default="USD")

    def __str__(self):
        return self.company_name or self.user.get_username()

class Subscription(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.customer} -> {self.plan}"

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="invoices")
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[("draft","Draft"),("open","Open"),("paid","Paid"),("void","Void")], default="draft")
    currency = models.CharField(max_length=10, default="USD")
    total_cents = models.PositiveIntegerField(default=0)

    def recompute_total(self):
        total = sum(item.amount_cents for item in self.items.all())
        self.total_cents = total
        self.save(update_fields=["total_cents"])

    def __str__(self):
        return f"Invoice #{self.pk} - {self.customer} - {self.status}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    unit_price_cents = models.IntegerField()
    amount_cents = models.IntegerField(editable=False, default=0)

    def save(self, *args, **kwargs):
        self.amount_cents = self.quantity * self.unit_price_cents
        super().save(*args, **kwargs)
        self.invoice.recompute_total()

    def __str__(self):
        return self.description

class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name="payments")
    amount_cents = models.PositiveIntegerField()
    paid_at = models.DateTimeField(default=timezone.now)
    provider = models.CharField(max_length=50, default="manual")
    reference = models.CharField(max_length=120, blank=True, default="")

    def __str__(self):
        return f"{self.amount_cents/100:.2f} for invoice {self.invoice_id}"
