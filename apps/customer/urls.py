from django.urls import path
from apps.customer.views import LoginPage, CustomerView

urlpatterns = [
    path('create/', CustomerView.as_view(), name='create_customer'),
    path("login/", LoginPage.as_view(), name="login"),
]