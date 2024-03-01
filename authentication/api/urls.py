from django.urls import path

from authentication.api.views import GetTokenView, LoginView, RegisterView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('get-token/', GetTokenView.as_view(), name='get_token'),
    path('login/', LoginView.as_view(), name='login'),
]
