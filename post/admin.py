from django.contrib import admin
from django.db.models.functions import Length

from .models import Post,Comment,CommentReplay,Category

from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory


admin.site.register(CommentReplay)


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'created_at']
    list_filter = ('is_public',)
    actions = ['enable_is_public']
    inlines = [CommentInline]

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.annotate(caption_long=Length('caption'))  # ✅ استفاده از ORM تابع

    # def caption_long(self, obj):
    #     return obj.caption_long  # ❗ حواست باشه از obj.caption_long استفاده کنی، نه len(obj.caption)
    #
    # caption_long.short_description = 'Caption Long'
    # caption_long.admin_order_field = 'caption_long'




class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Category)

admin.site.register(Category, CategoryAdmin)