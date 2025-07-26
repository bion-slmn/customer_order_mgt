# apps/customer/service.py
from django.shortcuts import get_object_or_404
import requests
from apps.customer.models import Customer
from apps.customer.serializer import CustomerSerializer
from customer_order import settings
from django.contrib.auth.models import User

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
    

    @staticmethod
    def exchange_code_for_token(code):
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
            "grant_type": "authorization_code"
        }
        return requests.post(token_url, data=data)
    
    @staticmethod
    def get_google_user_info(access_token):
        user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return requests.get(user_info_url, headers=headers)
    
    @staticmethod
    def create_or_update_customer_from_google(access_token: str):
        """
        Create or update a customer based on Google user info.
        """
        user_info_response = CustomerService.get_google_user_info(access_token)
        if user_info_response.status_code != 200:
            return None

        data = user_info_response.json()
        email = data.get("email")
        user, created = User.objects.get_or_create(email=email)
        if created:
            user.first_name = data.get("given_name", user.first_name)
            user.last_name = data.get("family_name", user.last_name)
            user.save()
        return user
