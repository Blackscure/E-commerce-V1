from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.db import IntegrityError
from categories.api.serializers import CategorySerializer

from categories.models import Category
from utils.paginator import CustomPaginator
from utils.permissions import IsAuthenticatedUser

class CategoryList(APIView):
    permission_classes = [IsAuthenticatedUser]
    def get(self, request):
        try:
            categories = Category.objects.all()
            paginator = CustomPaginator()
            result_page = paginator.paginate_queryset(categories, request)
            serializer = CategorySerializer(result_page, many=True, context={'request': request})
            response = paginator.get_paginated_response(serializer.data)
            response_data = response.data  # Use a different variable name to avoid conflicts

            return Response({
                "status": True,
                'message': 'Categories',
                "data": response_data
            })
        except Exception as e:
            return Response({
                'status': False,
                'message': 'Error retrieving categories',
                "error": str(e)
            })

    def post(self, request):
        
        data = request.data

        # Validate if required fields are present
        if not data.get('name') or not data.get('description'):
            return Response({'status': False, 'message': 'Name and description are required fields.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CategorySerializer(data=data)
        
        try:
            serializer.is_valid(raise_exception=True)
            category = serializer.save()

            # Include the created data in the response
            response_data = {
                'status': True,
                'message': 'Category created successfully',
                'data': {
                    'id': category.id,
                    'name': category.name,
                    'description': category.description,
                    # Include other fields as needed
                }
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'status': False, 'message': 'Category with the same name already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False, 'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryDetail(APIView):
    permission_classes = [IsAuthenticatedUser]
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response({'category': serializer.data})

    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            # Retrieve the updated category data
            updated_category = self.get_object(pk)
            updated_serializer = CategorySerializer(updated_category)

            return Response({
                'status': True,
                'message': 'Category updated successfully',
                'data': updated_serializer.data  # Include the updated data in the response
            })
        except IntegrityError:
            return Response({'status': False, 'message': 'Category with the same name already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False, 'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response({'status': True, 'message': 'Category deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
