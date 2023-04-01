# users/admin.py

from django.contrib import admin
from django.contrib.auth import get_user_model
from users.models import Follow

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "username",
        "first_name",
        "last_name",
        "email",
    )
    search_fields = ("username", "email", "last_name")
    list_filter = ("username", "email", "first_name", "last_name")


class FollowAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "author")
    list_filter = ("user", "author")
    search_fields = ("user__username", "user__email")


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
