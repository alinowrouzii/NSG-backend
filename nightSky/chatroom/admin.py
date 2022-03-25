from django.contrib import admin
from chatroom.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "get_username", "get_user_fullname", "text", "user_is_sender")
    
    @admin.display(description='username')
    def get_username(self, obj):
        return obj.user.username
    
    @admin.display(description='fullname')
    def get_user_fullname(self, obj):
        return obj.user.get_full_name()