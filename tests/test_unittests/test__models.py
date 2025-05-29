from django.test import TestCase
from apps.category.models import Category
from decimal import Decimal
from apps.product.models import Product
from django.contrib.auth.models import User
from apps.customer.models import Customer
from apps.order.models import Order



class CategoryModelTest(TestCase):

    def setUp(self):
        # Create root category
        self.root = Category.objects.create(name="Electronics")
        # Create child category
        self.laptop = Category.objects.create(name="Laptops", parent=self.root)
        # Create sub-child category
        self.gaming_laptop = Category.objects.create(name="Gaming Laptops", parent=self.laptop)

    def test_category_str(self):
        self.assertEqual(str(self.root), "Electronics")
        self.assertEqual(str(self.laptop), "Laptops")

    def test_category_hierarchy(self):
        self.assertIsNone(self.root.parent)
        self.assertEqual(self.laptop.parent, self.root)
        self.assertEqual(self.gaming_laptop.parent, self.laptop)

    def test_children_relationship(self):
        self.assertIn(self.laptop, self.root.children.all())
        self.assertIn(self.gaming_laptop, self.laptop.children.all())
        self.assertEqual(list(self.gaming_laptop.children.all()), [])

    def test_unique_name_constraint(self):
        with self.assertRaises(Exception):
            Category.objects.create(name="Electronics")

    def test_mptt_tree_structure(self):
        # Check if MPTT fields are populated
        self.root.refresh_from_db()
        self.laptop.refresh_from_db()
        self.gaming_laptop.refresh_from_db()

        self.assertTrue(self.root.is_root_node())
        self.assertEqual(self.root.get_descendant_count(), 2)
        self.assertEqual(list(self.root.get_descendants()), [self.laptop, self.gaming_laptop])
        self.assertEqual(list(self.laptop.get_descendants()), [self.gaming_laptop])


class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")

    def test_product_creation(self):
        product = Product.objects.create(
            name="Smartphone",
            description="Latest model with OLED display",
            price=Decimal("799.99"),
            category=self.category
        )

        self.assertEqual(product.name, "Smartphone")
        self.assertEqual(product.description, "Latest model with OLED display")
        self.assertEqual(product.price, Decimal("799.99"))
        self.assertEqual(product.category, self.category)
        self.assertEqual(str(product), "Smartphone")

    def test_blank_description_allowed(self):
        product = Product.objects.create(
            name="Tablet",
            description="",
            price=Decimal("399.99"),
            category=self.category
        )
        self.assertEqual(product.description, "")

    def test_null_description_allowed(self):
        product = Product.objects.create(
            name="Laptop",
            description=None,
            price=Decimal("1099.99"),
            category=self.category
        )
        self.assertIsNone(product.description)


class CustomerModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="johndoe",
            email="johndoe@example.com",
            password="testpass123"
        )

    def test_create_customer(self):
        customer = Customer.objects.create(user=self.user, phone_number="0712345678")
        self.assertEqual(customer.user.username, "johndoe")
        self.assertEqual(customer.phone_number, "0712345678")
        self.assertEqual(str(customer), "johndoe@example.com")

    def test_create_customer_without_phone(self):
        customer = Customer.objects.create(user=self.user)
        self.assertIsNone(customer.phone_number)

    def test_customer_user_one_to_one(self):
        customer = Customer.objects.create(user=self.user)
        self.assertEqual(self.user.customer_profile, customer)

    def test_user_deletion_deletes_customer(self):
        customer = Customer.objects.create(user=self.user)
        self.user.delete()
        self.assertEqual(Customer.objects.count(), 0)


class OrderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="janedoe",
            email="janedoe@example.com",
            password="securepass123"
        )

        self.category = Category.objects.create(name="Electronics")

        self.product1 = Product.objects.create(
            name="Keyboard",
            price=Decimal("49.99"),
            description="Mechanical keyboard",
            category=self.category
        )

        self.product2 = Product.objects.create(
            name="Mouse",
            price=Decimal("29.99"),
            description="Wireless mouse",
            category=self.category
        )

    def test_create_order_with_products(self):
        order = Order.objects.create(
            customer=self.user,
            total_amount=Decimal("79.98")
        )
        order.product.set([self.product1, self.product2])

        self.assertEqual(order.customer, self.user)
        self.assertEqual(order.total_amount, Decimal("79.98"))
        self.assertEqual(order.product.count(), 2)
        self.assertIn(self.product1, order.product.all())
        self.assertIn(self.product2, order.product.all())

    def test_str_method(self):
        order = Order.objects.create(
            customer=self.user,
            total_amount=Decimal("0.00")
        )
        self.assertEqual(str(order), f"Order {order.id}")

    def test_order_deletion_cascades(self):
        order = Order.objects.create(
            customer=self.user,
            total_amount=Decimal("20.00")
        )
        self.user.delete()
        self.assertEqual(Order.objects.count(), 0)
