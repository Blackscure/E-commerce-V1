# serializers.py
from rest_framework import serializers
from orders.models import Order, OrderItem

from products.api.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ('product', 'quantity', 'subtotal')

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'products', 'order_date', 'total_amount', 'items')
