from rest_framework import serializers

from post.serializer import PostSerializer
from user.models import User, Profile

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'full_name')


class ProfileSerializer(serializers.ModelSerializer):
    post = PostSerializer(many=True,read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'bio', 'image', 'post')
        extra_kwargs = {
            'user':{'read_only':True},
        }
