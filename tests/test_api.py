from django.urls import reverse
from django.contrib.auth.models import User, Group
from rest_framework.test import APITestCase
from rest_framework import status
from apps.billing.models import Plan

class APISmokeTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="pass")
        admin_group, _ = Group.objects.get_or_create(name="Admin")
        self.user.groups.add(admin_group)

    def auth(self):
        url = reverse("token_obtain_pair")
        res = self.client.post(url, {"username":"admin","password":"pass"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        token = res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_create_plan(self):
        self.auth()
        res = self.client.post("/api/plans/", {"name":"Pro","price_cents":1500,"currency":"USD","interval":"month"} , format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Plan.objects.filter(name="Pro").exists())
