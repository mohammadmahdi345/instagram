from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from django.core.cache import cache
from user.models import User

class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith("Bearer "):
            return None  # در صورت نبود توکن، ادامه درخواست بدون احراز هویت خواهد بود

        token = auth_header.split("Bearer ")[-1]  # گرفتن توکن از هدر

        try:
            decoded_token = AccessToken(token)  # بررسی و اعتبارسنجی توکن
            user = User.objects.get(id=decoded_token['user_id'])  # یافتن کاربر بر اساس توکن
        except Exception:
            raise AuthenticationFailed("Invalid or expired token")

        return (user, None)