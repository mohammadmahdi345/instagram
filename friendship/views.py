from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from friendship.models import Friendship
from friendship.serializer import UserSerializer
from instagram.authentication import CustomTokenAuthentication
from user.models import User
from django.shortcuts import get_object_or_404


class UserListView(APIView):
    """برای دیدت کاربر ها"""
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.filter(is_banned=False,is_staff=False,is_superuser=False) # فقط کاربرهای غیر ادمین و اونایی که بن نیستن
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RequestView(APIView):
    """فرستادن درخواست دنبال کردن به کاربر دیگه"""
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            user = get_object_or_404(User, pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if Friendship.objects.filter(request_from=request.user, request_to=user).exists():
            return Response({'detail': 'Friendship request already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            friendship = Friendship.objects.create(request_from=request.user, request_to=user) # یک شی از فرندشیپ میسازیم که کاربر درخواست دهنده و کاربری که بهش درخواست داده شده رو مشخص میکنیم
            return Response({'detail':'request sent'}, status=status.HTTP_200_OK)


class RequestListView(APIView):
    """دیدن درخواست های فرستاده شده به کاربر"""
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friendship = Friendship.objects.filter(request_to=request.user,is_accepted=False)
        users = [fr.request_from for fr in friendship] # گرفتن یوزر ها
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class AcceptView(APIView):
    """قبول کردن درخواست کاربر مشخص"""
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            user = get_object_or_404(User, pk=pk)
            friendship = Friendship.objects.filter(request_to=request.user,request_from=user,is_accepted=False).first()
        except (User.DoesNotExist, Friendship.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
        friendship.is_accepted = True
        friendship.followers += 1 # اضافه شدن به تعداد فالور ها
        friendship.save()
        return Response({'detail':'this user follow you'}, status=status.HTTP_202_ACCEPTED)


class FollowingUsersView(APIView):
    """کاربر های دنبال شده"""
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friendship = Friendship.objects.filter(request_from=request.user, is_accepted=True) # کاربر هایی که بهشون درخواست دنبال کردن فرستادیم و کاربر هم قبول کرده
        users = [fr.request_to for fr in friendship]
        serializer = UserSerializer(users, many=True)
        return Response({'users':serializer.data,
                        'fallowing':len(users)},
                        status=status.HTTP_200_OK)


class FollowersUsersView(APIView):
    """کاربرهای دنبال کننده"""
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friendship = Friendship.objects.filter(request_to=request.user, is_accepted=True) # کاربر هایی که به ما درخواست فرستادن و ما هم قبول کردیم
        users = [fr.request_from for fr in friendship]
        serializer = UserSerializer(users, many=True)
        return Response({'users': serializer.data,
                         'fallowers': len(users)},
                        status=status.HTTP_200_OK)













