from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import ProductService
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class ProductView(APIView):
    """
    API view to handle product operations.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id: str):
        """
        Retrieve a product by ID.
        """
        product = ProductService.view_product_details(product_id)
        return Response(product, status=status.HTTP_200_OK)
        

    def post(self, request, *args, **kwargs):
        """
        Create a new product.
        """
        data = request.data
        product = ProductService.create_product(data)
        return Response(product, status=status.HTTP_201_CREATED)
# Create your views here.
