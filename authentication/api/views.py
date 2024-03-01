from rest_framework import  permissions, views, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.views import APIView






from django.contrib.auth import get_user_model

from authentication.api.serializers import RegisterSerializer, UserSerializer

User=get_user_model()


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self,request):
        data=request.data
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return Response({
                'status':False,
                'message':'Provide valid details to register'
            },status=status.HTTP_400_BAD_REQUEST)
        first_name = data.get('first_name')
        last_name=data.get('last_name')
        email = data.get('email')
        password = data.get('password')

        user = User.objects.filter(email=email)
        if user.exists():
            return Response({
                'status':False,
                'message':'User with this email already exists'
            },status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create(username=email,first_name=first_name,last_name=last_name,email=email)
        user.set_password(password)
        user.save()
        serializer = UserSerializer(user)
        return Response({
            'status':True,
            'message':'Registration successful',
            'data':serializer.data
        },status=status.HTTP_201_CREATED)

class GetTokenView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        print(email)
        print(password)

        # Perform authentication
        user = authenticate(email=email, password=password)
          

        if user is None:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        # Authentication succeeded
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': UserSerializer(user).data
        }

        return Response(data, status=status.HTTP_200_OK)
