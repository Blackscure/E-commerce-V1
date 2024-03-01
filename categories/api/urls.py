# urls.py
from django.urls import path

from categories.api.views import CategoryDetail, CategoryList


urlpatterns = [
    path('create-categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
]
