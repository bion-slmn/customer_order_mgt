from .serializer import CategorySerializer
from .models import Category
from django.shortcuts import get_object_or_404
from apps.product.models import Product
from django.db.models import Avg



class CatergoryService:
    @staticmethod
    def create_category(validated_data):
        """
        Create a category. Supports nested categories if 'parent' is provided.
        Expected input: {'name': str, 'parent': int (optional)}
        """
        serializer = CategorySerializer(data=validated_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
    

    @staticmethod
    def view_category_desccendants(category_id):
        """
        Return all descendants (subcategories) of a given category.
        """
        descendants = CatergoryService._get_category_and_descendants(category_id)
        return descendants
        
    @staticmethod
    def get_category_products(category_id):
        """
        Return all products under the category and its descendants.
        """
        descendants = CatergoryService._get_category_and_descendants(category_id)
        all_category_ids = descendants.values_list('id', flat=True)
        products = Product.objects.filter(category_id__in=all_category_ids)
        return products
    
    @staticmethod
    def get_average_product_price(category_id):
        """
        Return the average price of all products in the category and its descendants.
        """
        product = CatergoryService.get_category_products(category_id)
        avg_price = product.aggregate(avg_price=Avg('price'))['avg_price']
        return avg_price


    @staticmethod
    def _get_category_and_descendants(category_id):
        """
        Internal helper to retrieve a category and its descendants.
        """
        category = get_object_or_404(Category, id=category_id)
        return category.get_descendants(include_self=True)
    
    