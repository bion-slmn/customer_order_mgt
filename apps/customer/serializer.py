# apps/customer/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from apps.customer.models import Customer


class UserSerializer(serializers.ModelSerializer):
    """Serializer for Django's built-in User model."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data: dict) -> User:
        """
        Create and return a new User instance.
        """
        return User.objects.create_user(**validated_data)


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for the Customer model, nested with User."""
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ['id', 'user']

    def create(self, validated_data: dict) -> Customer:
        """
        Create and return a new Customer with nested User creation.
        """
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        return Customer.objects.create(user=user)
