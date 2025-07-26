from urllib import response
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from urllib.parse import urljoin
from django.shortcuts import render
from django.views import View
import requests
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .service import CustomerService
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication




class CustomerView(APIView):
    """
    API endpoint to create a new customer.
    Requires authentication via token or session
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("Authenticated user:", request.user)
        print("Is authenticated:", request.user.is_authenticated)
        data = request.data
        customer = CustomerService.create_customer(data)
        return Response(customer, status=201)  


class GoogleLogin(SocialLoginView):
    """
    Handles the OAuth2 login flow with Google.
    Redirects users to Google's login and returns tokens via dj-rest-auth.
    """
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client


class GoogleLoginCallback(APIView):
    """
    Handles the callback from Google OAuth2 login.
    Expects a 'code' parameter in the query string, exchanges it for tokens.

    GET /auth/google/callback/?code=abc123
    """
    def get(self, request, *args, **kwargs):
        code = request.GET.get("code")
        print("Received code:", code)  # Debugging line

        if code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        response = CustomerService.exchange_code_for_token(code)
        
        access_token = response.json().get("access_token")
        if not access_token:
            return Response({"error": "Access token not found"}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomerService.create_or_update_customer_from_google(access_token)

        print("User created or updated:", user)  # Debugging line

        refresh = RefreshToken.for_user(user)
        jwt_tokens = {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user_id": user.id,
        }

        print("User created or updated:", user)

        return Response(jwt_tokens, status=status.HTTP_200_OK)
    
    



class LoginPage(View):
    """
    Serves the login HTML page with Google OAuth credentials injected into the context.

    GET /login/
    Renders:
        pages/login.html
    """
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "pages/login.html",
            {
                "google_callback_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
                "google_client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            },
        )
