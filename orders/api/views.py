# views.py
from sqlite3 import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from orders.api.serializers import OrderSerializer
from orders.models import Order

from utils.permissions import IsAuthenticatedUser
from django.core.mail import send_mail

class OrderCreateView(APIView):
    permission_classes = [IsAuthenticatedUser]

    def send_invoice_email(self, order):
        subject = 'Invoice for Your Order'
        message = f'Thank you for your order! Here is the breakdown:\n\n{order}'
        from_email = 'wekesabuyahi@gmail.com'

        # Check if the user associated with the order exists and has an email
        if order.user and order.user.email:
            to_email = [order.user.email]
            send_mail(subject, message, from_email, to_email, fail_silently=False)
            return True  # Indicate that the email was sent successfully
        else:
            return False  # Indicate that the email could not be sent

    def post(self, request):
        try:
            # Ensure that the user is authenticated
            if not request.user.is_authenticated:
                return Response({'status': False, 'message': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

            # Add the user to the request data
            request.data['user'] = request.user.id

            serializer = OrderSerializer(data=request.data)
            if serializer.is_valid():
                order = serializer.save()
               

                # Check if the user is associated with the order
                if self.send_invoice_email(order):
                    return Response({'status': True, 'message': 'Order created successfully'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'status': False, 'message': 'User email not available'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'status': False, 'message': 'Invalid data provided', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({'status': False, 'message': f'Error creating order: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def send_invoice_email(self, order):
        subject = 'Invoice for Your Order'
        message = f'Thank you for your order! Here is the breakdown:\n\n{order}'
        from_email = 'wekesabuyahi@gmail.com'

        # Check if the user associated with the order exists and has an email
        if order.user and order.user.email:
            to_email = [order.user.email]
            send_mail(subject, message, from_email, to_email, fail_silently=False)
            return True  # Indicate that the email was sent successfully
        else:
            return False  # Indicate that the email could not be sent

    def post(self, request):
        try:
            # Ensure that the user is authenticated
            if not request.user.is_authenticated:
                return Response({'status': False, 'message': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

            # Add the user to the request data
            request.data['user'] = request.user.id

            serializer = OrderSerializer(data=request.data)
            if serializer.is_valid():
                order = serializer.save()

                # Check if the user is associated with the order
                if self.send_invoice_email(order):
                    return Response({'status': True, 'message': 'Order created successfully'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'status': False, 'message': 'User email not available'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'status': False, 'message': 'Invalid data provided', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({'status': False, 'message': f'Error creating order: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderListCreateView(APIView):
    permission_classes = [IsAuthenticatedUser]
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response({'status': True, 'orders': serializer.data})
