from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import Plan, Customer, Subscription, Invoice, Payment
from .serializers import (
    PlanSerializer, CustomerSerializer, SubscriptionSerializer, InvoiceSerializer, PaymentSerializer
)
from .permissions import IsInGroup, ROLE_GROUPS, ReadOnly

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

    def get_permissions(self):
        if self.request.method in ("GET",):
            return [permissions.IsAuthenticated()]
        return [IsInGroup(groups=[ROLE_GROUPS["ADMIN"], ROLE_GROUPS["FINANCE"]])]

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.select_related("user").all()
    serializer_class = CustomerSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser or self.request.user.groups.filter(name__in=[ROLE_GROUPS["ADMIN"], ROLE_GROUPS["FINANCE"], ROLE_GROUPS["SUPPORT"]]).exists():
            return qs
        # Customers can only see their own profile
        return qs.filter(user=self.request.user)

    def get_permissions(self):
        if self.request.method in ("GET",):
            return [permissions.IsAuthenticated()]
        return [IsInGroup(groups=[ROLE_GROUPS["ADMIN"], ROLE_GROUPS["FINANCE"]])]

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.select_related("customer", "plan").all()
    serializer_class = SubscriptionSerializer

    def get_permissions(self):
        if self.request.method in ("GET",):
            return [permissions.IsAuthenticated()]
        return [IsInGroup(groups=[ROLE_GROUPS["ADMIN"], ROLE_GROUPS["FINANCE"]])]

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.prefetch_related("items").all()
    serializer_class = InvoiceSerializer

    def get_permissions(self):
        if self.request.method in ("GET",):
            return [permissions.IsAuthenticated()]
        return [IsInGroup(groups=[ROLE_GROUPS["ADMIN"], ROLE_GROUPS["FINANCE"]])]

    @action(detail=True, methods=["post"])
    def mark_paid(self, request, pk=None):
        invoice = self.get_object()
        serializer = PaymentSerializer(data={
            "invoice": invoice.id,
            "amount_cents": invoice.total_cents,
            "provider": "manual",
            "reference": request.data.get("reference", ""),
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        invoice.status = "paid"
        invoice.save(update_fields=["status"])
        return Response({"status": "paid"})

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsInGroup(groups=[ROLE_GROUPS["FINANCE"], ROLE_GROUPS["SUPPORT"]])]

