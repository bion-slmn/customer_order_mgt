from django.urls import path
from .views import (
    CategoryView,
    CategoryProductsView,
    CategoryAveragePriceView
)


urlpatterns = [
    path('create/', CategoryView.as_view(), name='category_create'),
    path('view/<str:category_id>/', CategoryView.as_view(), name='category_view'),
    path('products/<str:category_id>', CategoryProductsView.as_view(), name='category_products'),
    path('average-price/<str:category_id>', CategoryAveragePriceView.as_view(), name='average_price'),
]