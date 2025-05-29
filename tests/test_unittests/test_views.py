from apps.customer.models import Customer
from apps.order.models import Order

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.category.models import Category
from apps.product.models import Product
from django.conf import settings


class CategoryViewTests(APITestCase):
    def setUp(self):
        self.parent_category = Category.objects.create(name="Electronics")
        self.sub_category = Category.objects.create(name="Phones", parent=self.parent_category)

        self.product1 = Product.objects.create(
            name="Phone A",
            description="Basic phone",
            price=100,
            category=self.sub_category
        )
        self.product2 = Product.objects.create(
            name="Phone B",
            description="Advanced phone",
            price=300,
            category=self.sub_category
        )

    def test_create_category(self):
        url = reverse('category_create')
        data = {"name": "Computers", "parent": self.parent_category.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Computers")

    def test_view_category_descendants(self):
        url = reverse('category_view', args=[self.parent_category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Includes parent and child

    def test_view_category_products(self):
        url = reverse('category_products', args=[self.parent_category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], "Phone A")

    def test_average_product_price(self):
        url = reverse('average_price', args=[self.parent_category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_avg = (self.product1.price + self.product2.price) / 2
        self.assertEqual(float(response.data['average_price']), expected_avg)


class ProductViewTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=99.99,
            category=self.category
        )

    def test_create_product(self):
        url = reverse("create_product")
        data = {
            "name": "New Phone",
            "description": "Smartphone",
            "price": 499.99,
            "category": self.category.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Phone")
        self.assertEqual(Product.objects.count(), 2)

    def test_view_existing_product(self):
        url = reverse("view_product", args=[str(self.product.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)

    def test_view_nonexistent_product(self):
        url = reverse("view_product", args=["99999999-9999-9999-9999-999999999999"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from unittest.mock import patch



User = get_user_model()

class OrderViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client = APIClient()
        self.client.login(username="testuser", password="password123")

        self.category = Category.objects.create(name="Tech")
        self.product = Product.objects.create(
            name="Laptop",
            description="High-end laptop",
            price=1000.0,
            category=self.category
        )
        self.customer = Customer.objects.create(user=self.user, phone_number="1234567890")

    @patch("apps.order.views.django_rq.enqueue")
    def test_create_order(self, mock_enqueue):
        url = reverse("create_order")
        data = {
            "product": [str(self.product.id)],
            "total_amount": 20
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

    def test_view_order(self):
        order = Order.objects.create(
            customer=self.user,
            total_amount=100
        )
        self.client.force_authenticate(user=self.user)
        order.product.set([self.product])
        url = reverse("view_order", args=[str(order.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["product"], [self.product.id])

    def test_view_order_unauthenticated(self):
        self.client.logout()
        order = Order.objects.create(customer=self.user, total_amount=100)
        order.product.set([self.product])
        url = reverse("view_order", args=[str(order.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_create_order_unauthenticated(self):
        self.client.logout()
        url = reverse("create_order")
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CustomerViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('create_customer')

 
    def test_create_customer_success(self):
        
        payload = {'phone_number': '070102340', 'user': self.user.id}
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)

class LoginPageViewTests(APITestCase):
    def test_login_page_renders_with_context(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/login.html')
        self.assertIn('google_client_id', response.context)
        self.assertEqual(response.context['google_client_id'], settings.GOOGLE_OAUTH_CLIENT_ID)
        self.assertIn('google_callback_uri', response.context)
        self.assertEqual(response.context['google_callback_uri'], settings.GOOGLE_OAUTH_CALLBACK_URL)

