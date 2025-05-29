from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import OrderService
from rest_framework.permissions import IsAuthenticated
import django_rq
from notifications import send_order_email_to_admin, send_order_sms


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
        order_instance, order_serialised = OrderService.create_order(data)

        django_rq.enqueue(send_order_email_to_admin, order_instance, customer)
        django_rq.enqueue(send_order_sms, customer, order_instance.id)

        return Response(order_serialised, status=status.HTTP_201_CREATED)
    
    
# Create your views here.
