from django.contrib import admin
from blog.models import Post, Comment

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "timestamp")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "get_username", "get_user_fullname", "status", "timestamp")
    list_filter = ("timestamp", "status",)
    search_fields = ("user__username",)
    
    @admin.display(description='username')
    def get_username(self, obj):
        return obj.user.username

    @admin.display(description='fullname')
    def get_user_fullname(self, obj):
        return obj.user.get_full_name()
