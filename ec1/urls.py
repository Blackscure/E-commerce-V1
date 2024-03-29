from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('apps/ec1/api/v1/authentication/', include('authentication.api.urls')),
    path('apps/ec1/api/v1/categories/', include('categories.api.urls')),
    path('apps/ec1/api/v1/products/', include('products.api.urls')),
    path('apps/ec1/api/v1/customers/', include('customers.api.urls')),
    path('apps/ec1/api/v1/orders/', include('orders.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

