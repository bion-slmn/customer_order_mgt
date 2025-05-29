
from django.test import TestCase
from apps.category.models import Category
from apps.category.serializer import CategorySerializer
from apps.product.models import Product
from apps.product.serializer import ProductSerializer
from django.contrib.auth import get_user_model
from apps.customer.models import Customer
from apps.customer.serializer import CustomerSerializer
from django.utils import timezone
from apps.order.models import Order
from apps.order.serializer import OrderSerializer


User = get_user_model()

class CategorySerializerTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Beverages')

    def test_serialization(self):
        serializer = CategorySerializer(self.category)
        data = serializer.data

        self.assertEqual(data['id'], str(self.category.id))
        self.assertEqual(data['name'], 'Beverages')

    def test_deserialization_valid_data(self):
        data = {
            'name': 'Snacks'
        }
        serializer = CategorySerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        category = serializer.save()

        self.assertEqual(category.name, 'Snacks')

    def test_deserialization_invalid_data(self):
        data = {
            'name': ''  # assuming name is required
        }
        serializer = CategorySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)



class ProductSerializerTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name='Test Product',
            price=10.99,
            description='Test Description',
            category=self.category
        )

    def test_serialization(self):
        serializer = ProductSerializer(self.product)
        data = serializer.data
        
        # Check that id and timestamps are read-only and correctly formatted
        self.assertEqual(data['id'], str(self.product.id))
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
        
        self.assertEqual(data['name'], 'Test Product')
        self.assertEqual(float(data['price']), 10.99)
        self.assertEqual(data['description'], 'Test Description')

    def test_deserialization_valid_data(self):
        valid_data = {
            'name': 'New Product',
            'price': 20.50,
            'description': 'New Description',
            'category': self.category.id
        }
        serializer = ProductSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        product = serializer.save()
        self.assertEqual(product.name, 'New Product')
        self.assertEqual(product.price, 20.50)
        self.assertEqual(product.description, 'New Description')

    def test_deserialization_invalid_data(self):
        invalid_data = {
            'name': '',  # assuming name is required and cannot be blank
            'price': -10  # assuming price cannot be negative
        }
        serializer = ProductSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        # You can also check price validation errors if implemented


User = get_user_model()

class CustomerSerializerTestCase(TestCase):
    def setUp(self):
        # Create a user and customer instance for tests
        self.user = User.objects.create_user(username='testuser', password='pass1234')
        self.customer = Customer.objects.create(
            user=self.user,
            phone_number='1234567890',
        )

    def test_serialization(self):
        serializer = CustomerSerializer(self.customer)
        data = serializer.data
        
        self.assertEqual(data['id'], str(self.customer.id))
        self.assertEqual(data['user'], self.user.id)  # Assuming user is a FK and serialized as ID
        self.assertEqual(data['phone_number'], '1234567890')
        

    
        

    def test_deserialization_invalid_data(self):
        invalid_data = {
            'user': None,  # Assuming user is required
            'phone_number': '',
            'address': '',
        }
        serializer = CustomerSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('user', serializer.errors)
        self.assertIn('phone_number', serializer.errors)



class OrderSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass1234')
        self.customer = Customer.objects.create(user=self.user, phone_number='1234567890')
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name='Test Product',
            price=10.99,
            description='Test Description',
            category=self.category
        )

        # Create the order without products first
        self.order = Order.objects.create(
            customer=self.user,
            total_amount=200,
        )
        self.order.product.set([self.product])  # Many-to-many set

    def test_order_serialization(self):
        serializer = OrderSerializer(self.order)
        data = serializer.data

        self.assertEqual(data['id'], str(self.order.id))
        self.assertEqual(data['customer'], self.user.id)
        self.assertEqual(data['product'], [self.product.id])  # ManyToManyField returns a list
        self.assertEqual(data['total_amount'], '200.00')

    def test_order_deserialization_valid(self):
        valid_data = {
            'customer': self.user.id,
            'product': [self.product.id],  # must be a list for many-to-many
            'total_amount': 300,
        }
        serializer = OrderSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save()
        self.assertEqual(order.total_amount, 300)
        self.assertEqual(list(order.product.all()), [self.product])

    def test_order_deserialization_invalid(self):
        invalid_data = {
            'customer': None,
            'product': None,  # or leave it out entirely
            'total_amount': -50,
        }
        serializer = OrderSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('customer', serializer.errors)
        self.assertIn('product', serializer.errors)
       
