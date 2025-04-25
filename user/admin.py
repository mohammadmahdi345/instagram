# your_app/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # مدل کاربر خودتان
from django.utils.translation import gettext as _

class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', 'ban_or_not')
    actions = ['ban_users', 'unban_users']
    def ban_users(self, request, queryset):
        queryset.update(is_banned=True)
        self.message_user(request, "Selected users have been banned.")

    def unban_users(self, request, queryset):
        queryset.update(is_banned=False)
        self.message_user(request, "Selected users have been unbanned.")

    def ban_or_not(self, obj):
        return obj.is_banned





admin.site.register(User,MyUserAdmin)