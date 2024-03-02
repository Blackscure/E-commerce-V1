from django.urls import path

from products.api.views import ProductCreateView, ProductDetail, ProductList


urlpatterns = [
     path('create-product/', ProductCreateView.as_view(), name='product-list'),
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
]
