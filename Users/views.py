from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
from .models import Users

# Template view functions
def login_view(request):
    """Render the login page"""
    return render(request, 'users/login.html')

def register_view(request):
    """Render the registration page"""
    return render(request, 'users/registration.html')


# API endpoints
@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    """Handle user login via API"""
    try:
        print("Login request data:", request.data)
        
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({
                'message': 'Email and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Custom authentication for email-based login
        try:
            user = Users.objects.get(email=email)
            if user.check_password(password):
                if user.is_active:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({
                        'message': 'Login successful',
                        'token': token.key,
                        'user': UserSerializer(user).data
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'message': 'Account is disabled'
                    }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({
                    'message': 'Invalid email or password'
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Users.DoesNotExist:
            return Response({
                'message': 'Invalid email or password'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    except Exception as e:
        print("Login exception:", str(e))
        return Response({
            'message': 'Login failed',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    """Handle user registration via API"""
    try:
        print("Registration request data:", request.data)  # Debug print
        
        # Check if data is being received correctly
        if not request.data:
            return Response({
                'message': 'No data received'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = RegisterSerializer(data=request.data)
        print("Serializer created, checking validity...")  # Debug print
        
        if serializer.is_valid():
            print("Serializer is valid, creating user...")  # Debug print
            user = serializer.save()
            print(f"User created successfully: {user.username}, ID: {user.userID}")  # Debug print
            
            token, created = Token.objects.get_or_create(user=user)
            print(f"Token created: {token.key}")  # Debug print
            
            return Response({
                'message': 'Registration successful',
                'token': token.key,
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        else:
            print("Serializer validation errors:", serializer.errors)  # Debug print
            return Response({
                'message': 'Registration failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        print("Error during registration:", str(e))  # Debug print
        import traceback
        traceback.print_exc()  # This will show the full error traceback
        return Response({
            'message': 'Registration failed',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_api(request):
    """Handle user logout via API"""
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({
            'message': 'Token not found'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_api(request):
    """Get user profile via API"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)