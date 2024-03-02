# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from orders.api.serializers import OrderSerializer

from orders.models import Order


class OrderListCreateView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response({'status': True, 'orders': serializer.data})

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            self.send_invoice_email(order)
            return Response({'status': True, 'message': 'Order created successfully'}, status=status.HTTP_201_CREATED)
        return Response({'status': False, 'message': 'Invalid data provided', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def send_invoice_email(self, order):
        # Implement email sending logic here
        # You can use Django's send_mail function or a third-party library like Django Email Message
        # Example:
        subject = 'Invoice for Your Order'
        message = f'Thank you for your order! Here is the breakdown:\n\n{order}'
        from_email = 'your@example.com'
        to_email = [order.user.email]
        # send_mail(subject, message, from_email, to_email, fail_silently=False)
