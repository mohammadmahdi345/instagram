# your_project/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# تنظیمات Django رو وارد می‌کنیم
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instagram.settings')

app = Celery('instagram')

# بارگذاری تنظیمات Celery از تنظیمات Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# ثبت taskهای موجود
app.autodiscover_tasks()