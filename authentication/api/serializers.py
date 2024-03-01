from rest_framework import serializers
from authentication.models import User
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'sex', 'status', 'image', 'user_type', 'first_name', 'last_name')
        # Fields that should not be modified directly
        read_only_fields = ('id', 'username', 'email')

    def create(self, validated_data):
        # Retrieve the email from validated_data or use a default value
        email = validated_data.get('email', None)

        # Create the user with the provided data
        user = User.objects.create(
            username=email,  # Using email as username
            email=email,
            sex=validated_data.get('sex'),
            status=validated_data.get('status'),
            image=validated_data.get('image'),
            user_type=validated_data.get('user_type'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
        )

        # Set the password using set_password method
        user.set_password(validated_data.get('password'))
        user.save()

        return user