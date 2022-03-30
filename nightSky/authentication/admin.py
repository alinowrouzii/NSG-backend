from django.contrib import admin
from authentication.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

UserAdmin.fieldsets += ('Additional fields', {'fields': ('is_verified', 'phone_number', 'address', 'avatar')}),

admin.site.register(User, UserAdmin)
