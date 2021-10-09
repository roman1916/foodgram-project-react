from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Follow

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('pk', 'email', 'username')
    list_filter = ('email', 'username')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'following')
    list_filter = ['user', 'following']
