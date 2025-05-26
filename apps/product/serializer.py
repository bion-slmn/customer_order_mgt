from .models import Product
from customer_order.base_serializer import BaseSerializer
from rest_framework import serializers

class ProductSerializer(BaseSerializer):
    '''serializer of a product'''

    class Meta:
        model = Product
        fields = '__all__'