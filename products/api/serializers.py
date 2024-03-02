from rest_framework import serializers

from categories.api.serializers import CategorySerializer
from categories.models import Category
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'category', 'image')

    def validate_name(self, value):
        """
        Check if a product with the same name already exists.
        """
        existing_products = Product.objects.filter(name__iexact=value)
        if self.instance:
            existing_products = existing_products.exclude(pk=self.instance.pk)

        if existing_products.exists():
            raise serializers.ValidationError("A product with the same name already exists.")
        
        return value

    def create(self, validated_data):
        """
        Create a new product and return its data.
        """
        product = Product.objects.create(**validated_data)
        return product