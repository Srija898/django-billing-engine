from django.contrib import admin
from .models import Plan, Customer, Subscription, Invoice, InvoiceItem, Payment

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price_cents", "currency", "interval", "active")
    list_filter = ("active", "interval", "currency")

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "company_name", "default_currency")

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("customer", "plan", "start_date", "end_date", "active")
    list_filter = ("active", "plan")

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "created_at", "due_date", "status", "total_cents", "currency")
    list_filter = ("status", "currency")
    inlines = [InvoiceItemInline]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("invoice", "amount_cents", "paid_at", "provider", "reference")
