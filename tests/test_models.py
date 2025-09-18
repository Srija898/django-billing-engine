from django.test import TestCase
from django.contrib.auth.models import User
from apps.billing.models import Plan, Customer, Subscription, Invoice, InvoiceItem

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u1", password="pass")
        self.customer = Customer.objects.create(user=self.user, company_name="Acme")
        self.plan = Plan.objects.create(name="Basic", price_cents=999, currency="USD", interval="month")

    def test_invoice_total(self):
        sub = Subscription.objects.create(customer=self.customer, plan=self.plan)
        inv = Invoice.objects.create(customer=self.customer, due_date="2099-01-01", status="open", currency="USD")
        InvoiceItem.objects.create(invoice=inv, description="Sub Basic", quantity=2, unit_price_cents=500)
        inv.refresh_from_db()
        self.assertEqual(inv.total_cents, 1000)
