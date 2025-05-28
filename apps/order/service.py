from .serializer import OrderSerializer
from django.shortcuts import get_object_or_404
from .models import Order



class OrderService:
    @staticmethod
    def create_order(validated_data):
        """
        Create a corder. 
        """
        serializer = OrderSerializer(data=validated_data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return (order, serializer.data)
        
    

    @staticmethod
    def view_order(order_id):
        """
        Retrieve a single order by ID.
        """
        order = get_object_or_404(Order, id=order_id)
        return OrderSerializer(order).data

    @staticmethod
    def list_orders():
        """
        Retrieve all orders (optional helper).
        """
        orders = Order.objects.all()
        return OrderSerializer(orders, many=True).data