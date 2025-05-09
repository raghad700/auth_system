from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from .models import User

class RegisterView(APIView):
    """
    Handles user registration with email, password, and profile information.
    Returns JWT tokens upon successful registration.
    """
    def post(self, request):
        # Validate incoming data using UserSerializer
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            # Check for existing email (enforced by model but double-checking here)
            if User.objects.filter(email=serializer.validated_data['email']).exists():
                return Response(
                    {'error': 'Email already exists'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create new user (password gets hashed via User model's save())
            user = serializer.save()
            
            # Simulate welcome email (console output for demonstration)
            print("\n" + "="*50)
            print(f"A welcome email has been sent to: {user.email}")
            print(f"Hello {user.first_name} {user.last_name}!")
            print("Thank you for registering in our system")
            print("="*50 + "\n")
            
            # Generate JWT tokens for immediate authentication
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': serializer.data,  # Serialized user data
                'access': str(refresh.access_token),  # Short-lived access token
                'refresh': str(refresh)  # Long-lived refresh token
            }, status=status.HTTP_201_CREATED)
            
        # Return validation errors if data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """
    Handles user authentication using email and password.
    Returns JWT tokens upon successful login.
    """
    def post(self, request):
        # Extract credentials from request
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Debug logging (remove in production)
        print(f"Attempting login with email: {email}")
        
        try:
            # Find user by email (unique per model)
            user = User.objects.get(email=email)
            print(f"User found: {user.username}")
        except User.DoesNotExist:
            print("User not found")
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Debug password verification
        print(f"Stored password: {user.password}")
        print(f"Password check result: {user.check_password(password)}")
        
        # Verify password (handled by custom User model)
        if not user.check_password(password):
            print("Password check failed")
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generate new JWT tokens for authenticated session
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),  # For authenticating requests
            'refresh': str(refresh)  # For obtaining new access tokens
        })

class ProfileView(APIView):
    """
    Provides access to authenticated user's profile information.
    Requires valid JWT authentication.
    """
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access
    
    def get(self, request):
        # Serialize and return current user's data
        serializer = UserSerializer(request.user)
        return Response(serializer.data)