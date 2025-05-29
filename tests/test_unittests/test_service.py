from django.test import TestCase
from apps.category.models import Category
from apps.product.models import Product
from django.contrib.auth.models import User
from apps.customer.models import Customer
from apps.order.models import Order
from apps.category.service import CatergoryService
from apps.customer.service import CustomerService
from apps.product.service import ProductService
from apps.order.service import OrderService
from decimal import Decimal
from django.http import Http404




class CategoryServiceTestCase(TestCase):

    def setUp(self):
        self.parent_category = Category.objects.create(name="Electronics")
        self.sub_category = Category.objects.create(name="Phones", parent=self.parent_category)
        
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        self.product1 = Product.objects.create(
            name="iPhone",
            price=999.99,
            description="Apple phone",
            category=self.sub_category
        )
        self.product2 = Product.objects.create(
            name="Samsung",
            price=799.99,
            description="Samsung phone",
            category=self.sub_category
        )

    def test_create_category(self):
        data = {'name': 'Laptops', 'parent': self.parent_category.id}
        result = CatergoryService.create_category(data)

        self.assertEqual(result['name'], 'Laptops')
        self.assertEqual(Category.objects.filter(name='Laptops').count(), 1)

    def test_view_category_descendants(self):
        descendants = CatergoryService.view_category_desccendants(self.parent_category.id)
        self.assertIn(self.parent_category, descendants)
        self.assertIn(self.sub_category, descendants)

    def test_get_category_products(self):
        products = CatergoryService.get_category_products(self.parent_category.id)
        self.assertEqual(products.count(), 2)
        self.assertIn(self.product1, products)
        self.assertIn(self.product2, products)

    def test_get_average_product_price(self):
        avg_price = CatergoryService.get_average_product_price(self.parent_category.id)
        expected_avg = (self.product1.price + self.product2.price) / 2
        expected_avg = Decimal(str(expected_avg))
        self.assertAlmostEqual(avg_price, expected_avg)


class ProductServiceTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product_data = {
            "name": "Smartphone",
            "description": "Latest model smartphone.",
            "price": "499.99",
            "category": self.category.id
        }
        self.product = Product.objects.create(
            name="Laptop",
            description="Powerful laptop",
            price=Decimal("999.99"),
            category=self.category
        )

    def test_create_product(self):
        response = ProductService.create_product(self.product_data)
        self.assertEqual(response['name'], self.product_data['name'])
        self.assertEqual(response['price'], self.product_data['price'])

    def test_view_product_details(self):
        result = ProductService.view_product_details(self.product.id)
        self.assertEqual(result['id'], str(self.product.id))
        self.assertEqual(result['name'], "Laptop")

    def test_view_all_products(self):
        products = ProductService.view_all_products()
        self.assertIsInstance(products, list)
        self.assertGreaterEqual(len(products), 1)
        self.assertIn("Laptop", [p["name"] for p in products])


class CustomerServiceTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="1234567890"
        )

        self.user2 = User.objects.create(
            first_name="John",
            last_name="Doe",
            username="john.doe",
            password="1234567890"
        )
        self.valid_data = {
            "user": self.user.id,
            "phone_number": "0987654321"
        }


        self.customer = Customer.objects.create(user=self.user2, phone_number= "0987654321")

    def test_create_customer(self):
        result = CustomerService.create_customer(self.valid_data)
        self.assertEqual(result["phone_number"], "0987654321")
       

    def test_view_customer(self):
       
        result = CustomerService.view_customer(self.customer.id)
        self.assertEqual(result["phone_number"], "0987654321")

    def test_view_customer_invalid_id(self):
        with self.assertRaisesMessage(Exception, "No Customer matches the given query."):
            CustomerService.view_customer(9999)



class OrderServiceTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        # Create a customer
        self.customer = Customer.objects.create(user=self.user, phone_number="1234567890")
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Test Product",
            description="A test product",
            price=50.00,
            category=self.category  # or create a category if needed
        )
        # Sample order data
        self.valid_order_data = {
            "customer": self.user.id,
            "product": [self.product.id],
            "total_amount": 50.00,
        }

    def test_create_order(self):
        order, data = OrderService.create_order(self.valid_order_data)
        self.assertIsNotNone(order.id)
        self.assertEqual(data["total_amount"], "50.00")  # might be serialized as string

    def test_view_order(self):
        order, _ = OrderService.create_order(self.valid_order_data)
        fetched_order = OrderService.view_order(order.id)
        self.assertEqual(fetched_order["id"], str(order.id))

    def test_list_orders(self):
        OrderService.create_order(self.valid_order_data)
        OrderService.create_order(self.valid_order_data)
        orders = OrderService.list_orders()
        self.assertEqual(len(orders), 2)

    def test_view_order_not_found(self):
        with self.assertRaisesMessage(Http404, "No Order matches the given query."):
            OrderService.view_order(999)
