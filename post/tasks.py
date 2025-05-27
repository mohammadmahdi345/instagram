# yourapp/tasks.py
from celery import shared_task
from django.core.mail import send_mail

from friendship.models import Friendship
from .models import Post, User , Story

@shared_task
def send_post_notification_email(user_id, post_id):
    """تسک برای ایمیل زدن به دنبال کننده ها هنگام پست جدید"""
    try:
        user = User.objects.get(id=user_id)
        post = Post.objects.get(id=post_id)
        followers = Friendship.objects.filter(request_to=user, is_accepted=True)

        follower_users = [f.request_from for f in followers]

        for follower in follower_users:
            if follower.email and follower.receive_post_notifications:
                send_mail(
                    subject=f"کاربر {user.username} پست جدید گذاشت!",
                    message=f"عنوان پست: {post.title}\nتوضیح: {post.caption}",
                    from_email="no-reply@yourdomain.com",
                    recipient_list=[follower.email],
                    fail_silently=True
                )

    except Exception as e:
        print(f"[TASK ERROR]: {e}")


@shared_task
def send_story_notification_email(user_id):
    """تسک برای ایمیل زدن به دنبال کننده ها موثع استوری جدید"""
    try:
        from user.models import User  # اگر نیاز شد
        user = User.objects.get(id=user_id)

        story = Story.objects.filter(user=user).last()
        if not story or story.is_expired:
            return None# استوری منقضی شده یا وجود نداره

        followers = Friendship.objects.filter(request_to=user_id, is_accepted=True)

        follower_users = [f.request_from for f in followers]

        for user in follower_users:
            if user.email and user.receive_post_notifications:
                send_mail(
                    subject=f"کاربر {user.username} استوری جدید گذاشت!",
                    message="اگه تمایل داشتی ببینش!",
                    from_email="no-reply@yourdomain.com",
                    recipient_list=[user.email],
                    fail_silently=True
                )

    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)