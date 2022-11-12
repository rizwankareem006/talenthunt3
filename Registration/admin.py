from django.contrib import admin
from .models import ExtUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.

class ExtUserInline(admin.StackedInline):
    model = ExtUser
    can_delete = False
    verbose_name_plural = 'Extended User'

class UserAdmin(BaseUserAdmin):
    inlines = (ExtUserInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)