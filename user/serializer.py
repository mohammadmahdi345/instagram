from rest_framework import serializers

from post.serializer import PostSerializer
from .models import User, Profile, Bookmark


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'email', 'password')
        extra_kwargs = {
            'username':{'required':False},
            'password':{'write_only':True}
        }


class PasswordRecoverySerializer(serializers.ModelSerializer):
    """سریالایزر برای بازیابی پسورد"""

    class Meta:
        model = User
        fields = ['password']


class UserUpdateSerializer(serializers.ModelSerializer):
    """سریالایزر برای آپدیت اطلاعات"""

    class Meta:
        model = User
        fields = ('username','password','full_name')

# class LoginSerializer(serializers.ModelSerializer):
#     phone_number = serializers.CharField(required=False, validators=[])  # حذف UniqueValidator
#     email = serializers.EmailField(required=False, validators=[])
#     username = serializers.CharField(required=False, validators=[])
#
#     class Meta:
#         model = User
#         fields = ('username', 'phone_number', 'email', 'password')
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }
#
#
# class UserProfileSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Profile
#         fields =


class BookmarkSerializer(serializers.ModelSerializer):
    # post = PostSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = ('id', 'post', 'created_at')
        extra_kwargs = {
            'post': {'read_only': True}
                }

