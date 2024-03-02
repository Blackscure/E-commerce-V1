# views.py
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from customers.api.serializers import CustomerSerializer

from customers.models import Customer


class CustomerListCreateView(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response({'status': True, 'customers': serializer.data})

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'status': True, 'message': 'Customer created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'status': False, 'message': f'Error creating customer: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

class CustomerDetailView(APIView):
    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer)
        return Response({'status': True, 'customer': serializer.data})

    def put(self, request, pk):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'status': True, 'message': 'Customer updated successfully'})
        except Exception as e:
            return Response({'status': False, 'message': f'Error updating customer: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        customer = self.get_object(pk)
        customer.delete()
        return Response({'status': True, 'message': 'Customer deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
