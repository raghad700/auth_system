from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom User model.
    Handles user registration and data serialization.
    """
    
    password = serializers.CharField(write_only=True)  
    # Ensures password is write-only (won't be included in serialized output)
    # and handles proper field type for password input

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        # Specifies which fields should be included in the serialization
        # Includes both read-only (id) and writable fields

    def create(self, validated_data):
        """
        Creates and returns a new User instance.
        Uses Django's create_user helper for proper user creation.
        
        Args:
            validated_data: Dictionary containing validated user data
            
        Returns:
            User: The newly created user instance
        """
        user = User.objects.create_user(
            username=validated_data['username'],  # Required username
            email=validated_data['email'],        # Required email
            password=validated_data['password'],  # Password will be hashed via the User model's save()
            first_name=validated_data.get('first_name', ''),  # Optional first name
            last_name=validated_data.get('last_name', '')     # Optional last name
        )
        return user