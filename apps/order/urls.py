from django.urls import path
from .views import OrderView


urlpatterns = [
    path('create/', OrderView.as_view(), name="create_order"),
    path('view/<str:order_id>', OrderView.as_view(), name="view_order"),
]