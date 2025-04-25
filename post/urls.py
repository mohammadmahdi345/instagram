from django.urls import path
from .views import *
from rest_framework.routers import SimpleRouter, DefaultRouter

router = SimpleRouter()
router.register('post', PostView, basename='post')


router2 = SimpleRouter()
router2.register('category', CategoryView, basename='category')

# router3.register(r'category/admin', CategoryAdminView, basename='category-admin')
# router3 = DefaultRouter()

urlpatterns = [
    # path('posts/', PostView.as_view(), name='posts'),
    # path('post/<int:pk>/', PostDetailView.as_view(), name='post-Detail'),
    path('mypost/', MyPost.as_view(), name='my-post'),
    path('search/', Search.as_view(), name='search'),
    path('comments/<int:pk>/', CommentView.as_view(), name='comments'),
    path('comments/<int:pk>/', CommentReplayView.as_view(), name='comment-replay'),
    path('likes/<int:pk>/', LikeView.as_view(), name='like'),
    path('category/admin/', CategoryAdminView.as_view(), name='admin-category'),
    path('category/admin/<int:pk>/', CategoryAdminView2.as_view(), name='admin-category2'),
    path('stories/', StoryView.as_view(), name='stories'),
    path('bookmark/<int:pk>/', BookmarkView.as_view(), name='bookmark'),
    path('bookmark/', BookmarkGetView.as_view(), name='bookmark'),

] + router.urls + router2.urls
