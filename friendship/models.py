from django.db import models

class Friendship(models.Model):
    request_from = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='requested')
    request_to = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='requesting')
    is_accepted = models.BooleanField(default=False)
    fallowers = models.BigIntegerField(default=0)
    fallowing = models.BigIntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Friendship'
        verbose_name_plural = 'Friendships'

