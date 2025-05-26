from customer_order.base_serializer import BaseSerializer
from .models import Category


class CategorySerializer(BaseSerializer):
    ''' seralizer for category'''
    class Meta:
        model = Category
        fields = '__all__'