from django.urls import path
from .views import ProductView

urlpatterns = [
    path('create/', ProductView.as_view(), name="create_product"),
    path('view/<str:product_id>', ProductView.as_view(), name="view_product"),
]