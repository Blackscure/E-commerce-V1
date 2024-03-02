from django.urls import path

from products.api.serializers import ProductListCreateAPIView
from products.api.views import ProductDetailAPIView


urlpatterns = [
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
]
