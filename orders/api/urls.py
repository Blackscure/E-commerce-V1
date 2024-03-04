# urls.py
from django.urls import path

from orders.api.views import OrderCreateView, OrderListCreateView


urlpatterns = [
    path('create-order/', OrderCreateView.as_view(), name='order-create'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    # Add other URL patterns for retrieving, updating, and deleting orders
]
