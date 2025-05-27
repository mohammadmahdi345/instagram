from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Comment, CommentReplay, Post, Like, Category, Story


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {
            'user':{'read_only':True}
        }

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['user','post','text']
        extra_kwargs = {
            'user': {'read_only': True},
            'post': {'read_only': True}
        }


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('user', 'post', 'is_liked')
        extra_kwargs = {
            'user': {'read_only':True},
            'post': {'read_only': True},
            'is_liked': {'required':False}
        }

class CommentReplaySerializer(serializers.ModelSerializer):
    comment = CommentSerializer
    class Meta:
        model = CommentReplay
        fields = ('user', 'comment', 'text')
        extra_kwargs = {
            'user': {'read_only':True},
            'comment': {'read_only': True}
        }


class ChildCategory23Serializer(serializers.ModelSerializer):
    """"""
    class Meta:
        model = Category
        # در اینجا فقط فیلدهای مورد نیاز برای فرزند را می‌آوریم
        fields = ['id', 'title', 'description', 'slug']

class CategorySerializer(serializers.ModelSerializer):
    """سریالایزر کتگوری برای کاربران عادی"""

    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        if obj.is_root():

            children = obj.get_children() # اگر شی روت باشه(یعنی شبیه ریشه یک درخت) بچه هاش رو برمیگردونیم
            return ChildCategory23Serializer(children, many=True).data
        return []

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # اگر فرزند باشد، بخش children را حذف می‌کنیم
        if not instance.is_root():
            representation.pop('children', None)
        return representation

    class Meta:
        model = Category
        fields = ('title', 'description', 'slug', 'children')


class CategorySerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField

    def get_children(self, obj):
        if obj.is_root():
            children = obj.get_children()
            return ChildCategory23Serializer(children, many=True).data
        return []


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not instance.is_root():
            representation.pop('children', None)
        return representation
    
    class Meta:
        model = Category
        fields = ('title', 'description', 'slug', 'children')





class CategoryAdminPostSerializer(serializers.ModelSerializer):
    """برای ساخت کتگوری"""
    parent = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Category
        fields = ('id', 'title', 'description', 'is_public', 'slug', 'parent')

    def create(self, validated_data):
        parent = validated_data.pop('parent', None) # با توجه به اینکه پرنت مقدار داره یا نه حدس میزنیم کتگوری فرزنده یا والده
        if parent is None:
            instance = Category.add_root(**validated_data) # اگه برای هیچ والد مشخصی نبود یعنی یک والد جدیده
        else:
            parent_node = get_object_or_404(Category, pk=parent) #  والد رو میگیریم
            instance =  parent_node.add_child(**validated_data) # یک فرزند به ان اضافه میکنیم
        return instance



class AdminChildCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'description', 'is_public', 'path', 'depth', 'numchild']

class CategoryAdminGetSerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        children = obj.get_children()
        return CategoryAdminGetSerializer(children, many=True).data # بچه هارو تو بخش ادمین اینطور نشون میدیم(کل فیلد هارو برمیگردونیم)

    class Meta:
        model = Category
        fields = '__all__'

class CategoryAdminUpdateSerializer(serializers.ModelSerializer):
    """برای اپدیت فیلد های کتگوری"""

    class Meta:
        model = Category
        fields = ('id','title','description','is_public')


class StorySerializer(serializers.ModelSerializer):
    """سریالایزر برای استوری 24 ساعته"""

    class Meta:
        model = Story
        fields = ('user', 'story', 'created_at', 'is_expired')
        extra_kwargs = {
            'is_expired':{'read_only':True},
            'user': {'read_only': True}
        }