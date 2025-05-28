from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import OrderService
from rest_framework.permissions import IsAuthenticated


class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    """
    API view to handle order operations.
    """

    def get(self, request, order_id: str):
        """
        Retrieve an order by ID.
        """
        order = OrderService.view_order(order_id)
        return Response(order, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create a new order.
        """
        data = request.data.copy()
        customer = request.user
        data['customer'] = customer.id
        order = OrderService.create_order(data)
        return Response(order, status=status.HTTP_201_CREATED)
    
    
# Create your views here.
