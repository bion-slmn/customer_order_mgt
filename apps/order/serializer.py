from customer_order.base_serializer import BaseSerializer
from .models import Order


class OrderSerializer(BaseSerializer):
    class Meta:
        model = Order
        fields = '__all__'
