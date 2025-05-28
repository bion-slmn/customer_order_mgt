from django.contrib.auth.models import User
from customer_order.base_model import BaseModel
from django.db import models

class Customer(BaseModel):
    """Customer model representing a user in the system."""
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="customer_profile")

    def __str__(self):
        return self.user.email
