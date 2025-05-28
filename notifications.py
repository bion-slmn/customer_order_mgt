import africastalking
from django.conf import settings
from django.core.mail import send_mail

# Initialize Africa's Talking
africastalking.initialize('sandbox', settings.AFRICASTALKING_API_KEY)
sms = africastalking.SMS

def send_order_sms(phone_number, customer_name, order_id):
    """
    Send SMS notification to customer.
    """
    message = f"Hi {customer_name}, your order #{order_id} has been received. Thank you for shopping with us!"
    try:
        response = sms.send(message, [phone_number])
        return response
    except Exception as e:
        print(f"SMS sending failed: {e}")
        return None

def send_order_email_to_admin(order):
    """
    Send email notification to admin with order details.
    """
    subject = f"New Order #{order.id} Placed"
    message = (
        f"A new order has been placed.\n\n"
        f"Order ID: {order.id}\n"
        f"Customer: {order.customer.user.email}\n"
        f"Products:\n"
    )
    for item in order.products.all():
        message += f"- {item.name} (Price: {item.price})\n"
    message += f"\nTotal: {order.total_price()} " 

    send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.ADMIN_EMAIL])
