from django.contrib import admin
from authentication.models import User, ForgetRecord, VerificationCodeRecord
from django.contrib.auth.admin import UserAdmin

# Register your models here.

UserAdmin.fieldsets += ('Additional fields', {'fields': ('is_verified', 'phone_number', 'address', 'avatar')}),
UserAdmin.list_display += ('is_verified',)
admin.site.register(User, UserAdmin)




@admin.register(ForgetRecord)
class ForgetRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "get_username", "get_user_fullname", "code", "is_used", "expiration_date")
    search_fields = ("user__username",)
    
    @admin.display(description='username')
    def get_username(self, obj):
        return obj.user.username

    @admin.display(description='fullname')
    def get_user_fullname(self, obj):
        return obj.user.get_full_name()


@admin.register(VerificationCodeRecord)
class VerifyRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "get_username", "get_user_fullname", "code", "is_used")
    search_fields = ("user__username",)
    
    @admin.display(description='username')
    def get_username(self, obj):
        return obj.user.username

    @admin.display(description='fullname')
    def get_user_fullname(self, obj):
        return obj.user.get_full_name()