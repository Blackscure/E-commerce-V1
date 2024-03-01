from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from authentication.api.serializers import UserSerializer
from authentication.models import User
from django.db import IntegrityError


class RegistrationAPIView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': 'Provide valid details to register',
                'errors': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

        email = data.get('email')

        # Check if user with the provided email already exists
        user_exists = User.objects.filter(email=email).exists()
        if user_exists:
            return Response({
                'status': False,
                'message': 'User with this email already exists',
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create a new user
        user = serializer.save()

        # Serialize the user data for response
        user_serializer = self.serializer_class(user)

        return Response({
            'status': True,
            'message': 'Registration successful',
            'data': user_serializer.data,
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            user = User.objects.filter(username=username).first()
            if user and user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
