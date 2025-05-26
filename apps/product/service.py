from .serializer import ProductSerializer
from django.shortcuts import get_object_or_404
from .models import Product



class ProductService:
    @staticmethod
    def create_product(validated_data):
        """
        Create a product with its associated category.
        Expected input: dict with 'name', 'description', 'price', 'category_id'
        """
        serializer = ProductSerializer(data=validated_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
    
    @staticmethod
    def view_product_details(product_id):
        """
        Return details of a single product
        """
        product= get_object_or_404(Product, id=product_id)
        return ProductSerializer(product).data

    @staticmethod
    def view_all_products():
        """
        Return all products
        """
        products = Product.objects.all()
        return ProductSerializer(products, many=True).data
