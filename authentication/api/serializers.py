from rest_framework import serializers

from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'sex', 'status', 'image', 'user_type', 'first_name', 'last_name')
        # Fields that should not be modified directly
        read_only_fields = ('id', 'username', 'email')
        

    def validate_user_type(self, value):
        """
        Validate that the user_type is a valid choice.
        """
        choices = [choice[0] for choice in User.USER_TYPE]
        if value not in choices:
            raise serializers.ValidationError("Invalid user_type.")
        return value
