from datetime import timedelta

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from treebeard.mp_tree import MP_Node

from user.models import User, Profile, CreatedTime


class Category(MP_Node):
    title = models.CharField(max_length=255,db_index=True)
    description = models.CharField(max_length=500,blank=True,null=True)
    is_public = models.BooleanField(default=True)
    slug = models.SlugField()


    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


    def __str__(self):
        return self.title




class Post(CreatedTime):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    caption = models.TextField(max_length=512)
    file = models.FileField(upload_to='posts/post',blank=True,null=True)
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
    # created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title
def update_post(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.get(user=instance.user)
        profile.post.add(instance)
        profile.save()
post_save.connect(update_post, sender=Post)



class Comment(CreatedTime):
    post = models.ForeignKey(to=Post, on_delete=models.PROTECT, related_name='comments')
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_comment')
    text = models.TextField(max_length=512)

    is_approved = models.BooleanField(default=False)

    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.text


class CommentReplay(CreatedTime):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(to=Comment, on_delete=models.PROTECT,related_name='replays')
    text = models.TextField(max_length=512)
    # created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'CommentReplay'
        verbose_name_plural = 'CommentReplays'

    def __str__(self):
        return self.user



class Like(CreatedTime):
    post = models.ForeignKey(to=Post, on_delete=models.PROTECT, related_name='likes')
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=True)
    # created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

from django.utils import timezone

class Story(CreatedTime):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='stories')
    story = models.FileField(upload_to='stories/story')
    # created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def is_expired(self):
        # طول عمر 24 ساعت
        return timezone.now() > self.created_at + timedelta(hours=24)