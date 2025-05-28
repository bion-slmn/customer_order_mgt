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


class CustomerView(APIView):
    """
    API endpoint to create a new customer.
    Requires authentication via token or session
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        customer = CustomerService.create_customer(data)
        return Response(customer, status=201)  # fixed typo: 'Resposse' -> 'Response'


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

        if code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        token_endpoint_url = urljoin("http://localhost:8000", reverse("google_login"))
        response = requests.post(url=token_endpoint_url, data={"code": code})

        return Response(response.json(), status=status.HTTP_200_OK)


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
