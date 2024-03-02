from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from products.models import Product


class ProductDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if product:
            serializer = ProductSerializer(product)
            return Response({'product': serializer.data})
        return Response({'status': False, 'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        product = self.get_object(pk)
        if product:
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': True, 'message': 'Product updated successfully'})
            return Response({'status': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': False, 'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        product = self.get_object(pk)
        if product:
            product.delete()
            return Response({'status': True, 'message': 'Product deleted successfully'})
        return Response({'status': False, 'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
