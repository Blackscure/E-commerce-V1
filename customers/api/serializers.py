from rest_framework import serializers

from authentication.api.serializers import UserSerializer
from customers.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Assuming you have a UserSerializer

    class Meta:
        model = Customer
        fields = ('id', 'user', 'shipping_address', 'phone_number')
