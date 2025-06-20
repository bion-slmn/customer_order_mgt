import africastalking
from django.conf import settings
from django.core.mail import send_mail
from dotenv import load_dotenv
import os 

load_dotenv()

API_KEY = os.getenv('AFRICA_TALKING_API_KEY')
if not API_KEY:
    raise ValueError("AFRICA_TALKING_API_KEY is not set in the environment variables.")

africastalking.initialize('sandbox', API_KEY)

sms = africastalking.SMS

def send_order_sms(customer, order_id):
    """
    Send SMS notification to customer.
    """
    customer_name = customer.first_name
    phone_number = customer.customer_profile.phone_number

    if not phone_number:
        return

    message = f"Hi {customer_name}, your order #{order_id} has been received. Thank you for shopping with us!"
    try:
        response = sms.send(message, [phone_number])
        return response
    except Exception as e:
        print(f"SMS sending failed: {e}")
        return None

def send_order_email_to_admin(order, customer):
    """
    Send email notification to admin with order details.
    """
    subject = f"New Order #{order.id} Placed"
    message = (
        f"A new order has been placed.\n\n"
        f"Order ID: {order.id}\n"
        f"Customer: {customer.email}\n"
        f"Products:\n"
    )
    for item in order.product.all():
        message += f"- {item.name} (Price: {item.price})\n"
    message += f"\nTotal: {order.total_amount} " 


    send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.ADMIN_USER_EMAIL])
