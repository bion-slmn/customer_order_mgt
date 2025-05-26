from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils import timezone
from customer_order.base_model import BaseModel



class Category(MPTTModel, BaseModel):
    """Category model for hierarchical categorization."""
    name = models.CharField(max_length=255, unique=True, verbose_name="Category Name")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']


    def __str__(self):
        return self.name