from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect,HttpResponseRedirect
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from django.contrib import messages
from django.shortcuts import get_object_or_404
# from delino.authentication import CustomTokenAuthentication


import random

from friendship.serializer import ProfileSerializer
from instagram.authentication import CustomTokenAuthentication
from .models import User, Profile
from .serializer import RegisterSerializer, PasswordRecoverySerializer, UserUpdateSerializer#, LoginSerializer


class LoginView(APIView):
    def post(self,request):
        username = request.data.get('username')
        phone_number = request.data.get('phone_number')
        email = request.data.get('email')
        password = request.data.get('password')

        if not password:
            return Response({'detail': 'enter a password'}, status=status.HTTP_400_BAD_REQUEST)

        user= None
        if username:
            try:
                user = authenticate(request,username=username,password=password)
            except User.DoesNotExist:
                return Response({'detail':'username or password is wrong'})
        elif phone_number:
            user = User.objects.filter(phone_number=phone_number).first()
        elif email:
            user = User.objects.filter(email=email).first()
        else:
            return Response({'detail': 'Enter username or phone_number or email'}, status=status.HTTP_400_BAD_REQUEST)

        if user and user.check_password(password):
            if user.is_banned == False:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'detail': 'login successful',
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh)
                })
            else:
                return Response({'detail':'you banned in past'}, status=status.HTTP_403_FORBIDDEN)

        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



import uuid

def generate_unique_username():
    while True:
        username = "user_" + uuid.uuid4().hex[:8]  # مثل: user_3fae12dc
        if not User.objects.filter(username=username).exists():
            return username



class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        if not username:
            username = generate_unique_username()

        phone = serializer.validated_data.get('phone_number')
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')


        user = None

        if phone:
            user = User.objects.filter(phone_number=phone).first()
        elif email:
            user = User.objects.filter(email=email).first()
        if user:
            if user.check_password(password):
                if user.is_banned == False:
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'detail': 'login successful',
                        'access_token': str(refresh.access_token),
                        'refresh_token': str(refresh)
                    })
                else:
                    return Response({'detail': 'you banned in past'}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'detail':'password is wrong'},status=status.HTTP_401_UNAUTHORIZED)
        user = User.objects.create_user(username=username, phone_number=phone, email=email, password=password)
        refresh = RefreshToken.for_user(user)

        return Response({
            'detail': 'register successful',
            'username': username,  # به کاربر اعلام کن چی براش ساختی
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }, status=status.HTTP_201_CREATED)








class UserView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self,request):
        user = User.objects.get(id=request.user.id)
        if user:
            serializer = UserUpdateSerializer(user,data=request.data)
            if serializer.is_valid(raise_exception=True):
                # full_name = serializer.validated_data['full_name']
                # password = serializer.validated_data['password']
                # email = serializer.validated_data['email']
                serializer.save()
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UpdateUserPasswordView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self,request):
        user = User.objects.get(id=request.user.id)
        serializer = PasswordRecoverySerializer(user,data=request.data)

        if serializer.is_valid():
            # متد set_password پسورد را هش می‌کند
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'detail':'Password changed successfully.'},
                            status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class BanUserView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.is_banned = True
            user.save()
            return Response({"detail": f"{user.username} has been banned."})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


class UserProfileView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            profile = Profile.objects.get(user=user)
        except (User.DoesNotExist, Profile.DoesNotExist):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileGetView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


