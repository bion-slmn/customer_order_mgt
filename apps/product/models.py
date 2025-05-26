from django.db import models
from customer_order.base_model import BaseModel
from ..category.models import Category

# Create your models here.

class Product(BaseModel):
    """Product model for managing products in the system."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')


    def __str__(self):
        return self.name