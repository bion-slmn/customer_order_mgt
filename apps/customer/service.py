# apps/customer/service.py
from django.shortcuts import get_object_or_404
from apps.customer.models import Customer
from apps.customer.serializer import CustomerSerializer

class CustomerService:

    @staticmethod
    def create_customer(data):
        """
        Creates a new Customer 
        """
        serializer = CustomerSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    @staticmethod
    def view_customer(customer_id):
        """
        Fetch a customer by ID.
        """
        customer = get_object_or_404(Customer, id=customer_id)
        return CustomerSerializer(customer).data
