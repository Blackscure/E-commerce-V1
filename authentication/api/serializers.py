from rest_framework import serializers
from ..models import  User

class  UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =  User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_admin', 'created_at')


class RegisterSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', )
    