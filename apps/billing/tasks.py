from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Subscription, Invoice, InvoiceItem

@shared_task
def generate_invoices():
    today = timezone.now().date()
    due = today + timedelta(days=14)
    created = 0

    subs = Subscription.objects.filter(active=True).select_related("customer", "plan")
    for sub in subs:
        # Idempotent-ish example: do not create if open invoice exists for this month
        existing = Invoice.objects.filter(
            customer=sub.customer, status__in=["draft","open"], created_at__date__gte=today.replace(day=1)
        ).exists()
        if existing:
            continue
        inv = Invoice.objects.create(
            customer=sub.customer, due_date=due, status="open", currency=sub.customer.default_currency or sub.plan.currency
        )
        InvoiceItem.objects.create(
            invoice=inv, description=f"Subscription {sub.plan.name}", quantity=1, unit_price_cents=sub.plan.price_cents
        )
        inv.recompute_total()
        created += 1
    return {"created": created}
