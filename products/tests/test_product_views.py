from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from users.models import User


class ProductTests(APITestCase):
    def setUp(self):
        self.seller = User.objects.create_user(email="seller@example.com", password="pass", is_seller=True)
        self.customer = User.objects.create_user(email="cust@example.com", password="pass", is_customer=True)
        self.product_url = reverse("product-list-create")

    def test_customer_cannot_create_product(self):
        self.client.force_authenticate(user=self.customer)
        data = {"name": "Phone", "price": 1000}
        response = self.client.post(self.product_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_seller_can_create_product(self):
        self.client.force_authenticate(user=self.seller)
        data = {"name": "Laptop", "price": 2000}
        response = self.client.post(self.product_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
