

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from instagram.authentication import CustomTokenAuthentication
from user.models import Bookmark
from user.serializer import BookmarkSerializer
from .models import Post, Comment, Category, Story
from .serializer import PostSerializer, CommentSerializer, LikeSerializer, CommentReplaySerializer, CategorySerializer, \
    CategoryAdminPostSerializer, CategoryAdminGetSerializer, CategoryAdminUpdateSerializer, StorySerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .tasks import send_post_notification_email


class PostView(ModelViewSet):
    """قابلیت اجرای 4 متود اصلی"""

    serializer_class = PostSerializer
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(is_active=True,is_public=True) # فقظ پست هایی که فعال و عمومی باشن

    def perform_create(self, serializer):
        post = serializer.save(user=self.request.user)



class MyPost(APIView):
    """دیدن پست های خود کاربر"""
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            posts = Post.objects.filter(user=request.user,is_public=True)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class Search(APIView):
    """سرچ در بین اسم کاربر ها و عنوان پست ها """
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        search = request.data.get('search')
        search = Post.objects.filter(Q(user__username__icontains=search) | Q(title__icontains=search))
        serializer = PostSerializer(search,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class CommentView(APIView):
    """کامنت برای پست مورد نظر"""
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        comments = post.comments.filter(is_approved=True)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request,pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user,post=post)
            return Response({'detail': 'your comment sabt shod!!'}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LikeView(APIView):
    """لایک یک پست"""
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        likes = post.likes.filter(is_liked=True).count()
        return Response({'likes':likes})

    def post(self,request,pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user,post=post)
            return Response({'detail':'is liked'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CommentReplayView(APIView):
    """ریپلای به یک کامنت"""
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_comment(self, pk):
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return comment

    def get(self, request, pk):
        comment = self.get_comment(pk=pk)
        if not comment:
            return Response(status=status.HTTP_404_NOT_FOUND)
        replay = comment.replays.all()
        serializer = CommentReplaySerializer(replay, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request, pk):
        comment = self.get_comment(pk=pk)
        if not comment:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentReplaySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(comment=comment, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryView(viewsets.ReadOnlyModelViewSet):
    """ویو کتگوری برای کاربران عادی"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# class CategoryAdminView(viewsets.ModelViewSet):
#     authentication_classes = [CustomTokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     queryset = Category.objects.all()
#     serializer_class = CategoryAdminSerializer
#
#     # def get_serializer_class(self):
#     #     match self.action:
#     #         case 'create':
#     #             return CategoryAdminSerializer

# @method_decorator(csrf_exempt, name='dispatch')
class CategoryAdminView(APIView):
    """ویو کتگوری مخصوص ادمین"""
    permission_classes = [IsAdminUser]
    # authentication_classes = [CustomTokenAuthentication]

    def get(self,request):
        categories = Category.get_root_nodes() # دسته هایی رو میگیریم که هیچ والدی ندارند
        serializer = CategoryAdminGetSerializer(categories,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategoryAdminPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail':'category created!'},status=status.HTTP_200_OK)

# @method_decorator(csrf_exempt, name='dispatch')
class CategoryAdminView2(APIView):
    """ اپدیت کتگوری و دیدن شاخه خاص  وپاک کردن یک شاخه خاص"""
    permission_classes = [IsAdminUser]
    # authentication_classes = [CustomTokenAuthentication]

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategoryAdminGetSerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategoryAdminUpdateSerializer(category,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'category updated!'}, status=status.HTTP_200_OK)


    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response({'detail':'category deleted'},status=status.HTTP_200_OK)


class StoryView(APIView):
    """استوری 24 ساعته"""
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = StorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({'detail':'story added'}, status=status.HTTP_200_OK)

    def get(self, request):
        timezon = timezone.now() - timedelta(hours=24)
        qs = Story.objects.filter(created_at__gte=timezon).order_by('-created_at') # فیلتر استوری هایی که زمان ساختشون بزرگتر 24 ساعت پیشه
        serializer = StorySerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class BookmarkView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """
        ذخیره‌ی یک پست
        یا حذف کردنش
        POST /api/bookmarks/{post_id}/
        """
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            post=post
        )
        if not created:
            return Response({'detail': 'Already bookmarked.'},
                            status=status.HTTP_200_OK)

        serializer = BookmarkSerializer(bookmark)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        """
        لغو ذخیره‌ی یک پست
        DELETE /api/bookmarks/{post_id}/
        """
        try:
            bookmark = Bookmark.objects.get(user=request.user, pk=pk)
        except Bookmark.DoesNotExist:
            return Response({'detail': 'Bookmark not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        bookmark.delete()
        return Response({'detail': 'Bookmark removed.'},
                        status=status.HTTP_204_NO_CONTENT)


class BookmarkGetView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        فهرست پست‌های ذخیره‌شده کاربر
        GET /api/bookmarks/
        """
        qs = Bookmark.objects.filter(user=request.user)
        serializer = BookmarkSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
