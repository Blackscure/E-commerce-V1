# serializers.py
from rest_framework import serializers

from categories.models import Category
from products.models import Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')




class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'category', 'image')

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category_id = category_data.get('id')

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise serializers.ValidationError(f"Category with ID {category_id} does not exist.")

        product = Product.objects.create(category=category, **validated_data)
        return product
    
# create product
class ProductCreateSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'category_id', 'image')

    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
        category, _ = Category.objects.get_or_create(id=category_id)
        product = Product.objects.create(category=category, **validated_data)
        return product
    

