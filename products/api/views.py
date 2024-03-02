from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.api.serializers import ProductCreateSerializer, ProductSerializer

from products.models import Product
from utils.paginator import CustomPaginator


class ProductCreateView(APIView):
    def post(self, request):
        try:
            serializer = ProductCreateSerializer(data=request.data)
            if serializer.is_valid():
                product = serializer.save()
                response_data = {
                    'status': True,
                    'message': 'Product created successfully',
                    'data': ProductCreateSerializer(product).data
                }
                return Response(response_data, status=status.HTTP_201_CREATED)

            return Response({
                'status': False,
                'message': 'Invalid data provided',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'status': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProductList(APIView):
   def get(self, request):
        try:
            products = Product.objects.all()
            paginator = CustomPaginator()
            result_page = paginator.paginate_queryset(products, request)
            serializer = ProductSerializer(result_page, many=True, context={'request': request})
            response = paginator.get_paginated_response(serializer.data)
            response_data = response.data

            return Response({
                "status": True,
                'message': 'Products',
                "data": response_data
            })
        except Exception as e:
            return Response({
                'status': False,
                'message': 'Error retrieving products',
                "error": str(e)
            })


class ProductDetail(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        try:
            product = self.get_object(pk)
            serializer = ProductSerializer(product)
            return Response({'status': True, 'product': serializer.data})
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            product = self.get_object(pk)
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': True, 'message': 'Product updated successfully'})
            return Response({'status': False, 'message': 'Invalid data provided', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            product = self.get_object(pk)
            product.delete()
            return Response({'status': True, 'message': 'Product deleted successfully'})
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)