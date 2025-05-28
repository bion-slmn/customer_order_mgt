from django.db import models
from customer_order.base_model import BaseModel
from apps.product.models import Product
from django.contrib.auth.models import User

# Create your models here.


class Order(BaseModel):
    """Order model for managing customer orders."""
    product = models.ManyToManyField(Product, related_name='products')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='customer')
    
    

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"
