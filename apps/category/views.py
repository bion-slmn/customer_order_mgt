from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import CatergoryService
from .serializer import CategorySerializer
from ..product.serializer import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication



class CategoryView(APIView):
    """
    API view to handle category operations.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, category_id:str):
        """
        Retrieve a category by ID, including its descendants.
        """
        categories = CatergoryService.view_category_desccendants(category_id)
        all_categories = CategorySerializer(categories, many=True).data
        return Response(all_categories, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create a new category.
        """
        data = request.data
        category = CatergoryService.create_category(data)
        return Response(category, status=status.HTTP_201_CREATED)
    

class CategoryProductsView(APIView):
    """
    API view to handle product retrieval under a category.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, category_id:str):
        """
        Retrieve all products under a category and its descendants.
        """
        products = CatergoryService.get_category_products(category_id)
        all_products = ProductSerializer(products, many=True).data
        return Response(all_products, status=status.HTTP_200_OK)


class CategoryAveragePriceView(APIView):
    """
    API view to handle average product price retrieval under a category.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, category_id:str):
        """
        Retrieve the average price of products in a category and its descendants.
        """
        avg_price = CatergoryService.get_average_product_price(category_id)
        return Response({"average_price": avg_price}, status=status.HTTP_200_OK)