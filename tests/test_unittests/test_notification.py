from unittest import TestCase
from unittest.mock import patch, MagicMock
from notifications import send_order_sms, send_order_email_to_admin

class DummyProfile:
    def __init__(self, phone_number):
        self.phone_number = phone_number

class DummyCustomer:
    def __init__(self, first_name, phone_number, email="john@example.com"):
        self.first_name = first_name
        self.email = email
        self.customer_profile = DummyProfile(phone_number)

class DummyProduct:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class DummyOrder:
    def __init__(self, id, products, total_amount):
        self.id = id
        self.total_amount = total_amount
        self.product = MagicMock()
        self.product.all.return_value = products

class NotificationTests(TestCase):
    
    @patch('notifications.sms.send')
    def test_send_order_sms_success(self, mock_send):
        customer = DummyCustomer(first_name="Jane", phone_number="+254700000000")
        order_id = "abc123"
        mock_send.return_value = {"SMSMessageData": "Success"}

        result = send_order_sms(customer, order_id)
        
        self.assertEqual(result, {"SMSMessageData": "Success"})
        mock_send.assert_called_once_with(
            f"Hi Jane, your order #{order_id} has been received. Thank you for shopping with us!",
            ["+254700000000"]
        )

    @patch('notifications.sms.send')
    def test_send_order_sms_no_phone(self, mock_send):
        customer = DummyCustomer(first_name="Jane", phone_number=None)
        result = send_order_sms(customer, "abc123")
        self.assertIsNone(result)
        mock_send.assert_not_called()

    @patch('notifications.send_mail')
    def test_send_order_email_to_admin(self, mock_send_mail):
        customer = DummyCustomer(first_name="John", phone_number="+254712345678")
        products = [
            DummyProduct("Laptop", 1200),
            DummyProduct("Mouse", 25)
        ]
        order = DummyOrder("order123", products, total_amount=1225)

        send_order_email_to_admin(order, customer)

        mock_send_mail.assert_called_once()
