# views.py (accounts app)
# Handles user registration, login and password reset API endpoints.
# Registration creates a new user with username, email and password.
# Login returns a JWT access token and refresh token.
# Password reset sends a reset link to the user's email.

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({'error': 'Please provide username, email and password'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    refresh = RefreshToken.for_user(user)

    return Response({
        'message': 'Account created successfully!',
        'username': user.username,
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Please provide username and password'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.check_password(password):
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)

    return Response({
        'message': f'Welcome back, {user.username}!',
        'username': user.username,
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    # Get email from request
    email = request.data.get('email')

    if not email:
        return Response({'error': 'Please provide your email'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if user exists with this email
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Don't reveal if email exists or not for security
        return Response({'message': 'If this email is registered you will receive a reset link shortly!'})

    # Generate reset token
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    # Reset link pointing to frontend
    reset_link = f'http://localhost:5173/reset-password?uid={uid}&token={token}'

    # Send email
    send_mail(
        subject='Football Draft Helper — Password Reset',
        message=f'Hi {user.username},\n\nClick the link below to reset your password:\n\n{reset_link}\n\nIf you did not request this, ignore this email.\n\nFootball Draft Helper Team',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )

    return Response({'message': 'If this email is registered you will receive a reset link shortly!'})


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    uid = request.data.get('uid')
    token = request.data.get('token')
    new_password = request.data.get('password')

    if not uid or not token or not new_password:
        return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Decode user id
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
    except Exception:
        return Response({'error': 'Invalid reset link'}, status=status.HTTP_400_BAD_REQUEST)

    # Verify token
    if not default_token_generator.check_token(user, token):
        return Response({'error': 'Reset link is invalid or has expired'}, status=status.HTTP_400_BAD_REQUEST)

    # Set new password
    user.set_password(new_password)
    user.save()

    return Response({'message': 'Password reset successfully! You can now login.'})

    import requests as http_requests

@api_view(['GET'])
@permission_classes([AllowAny])
def get_news(request):
    # Fetch latest football news from NewsAPI
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': 'Premier League football',
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': 10,
        'apiKey': '6da5c23715be427c98a79be01ef21ca5'
    }
    response = http_requests.get(url, params=params)
    data = response.json()
    return Response(data)