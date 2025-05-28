# apps/customer/serializers.py
from rest_framework import serializers
from apps.customer.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for the Customer model, nested with User."""

    class Meta:
        model = Customer
        fields = "__all__"
