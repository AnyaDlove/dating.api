from django.contrib import admin

from .models import Invitation, Like, Photo, ProfileView


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "is_main", "uploaded_at")
    list_filter = ("is_main",)
    search_fields = ("user__username",)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "from_user", "to_user", "kind", "created_at")
    list_filter = ("kind",)
    search_fields = ("from_user__username", "to_user__username")


@admin.register(ProfileView)
class ProfileViewAdmin(admin.ModelAdmin):
    list_display = ("id", "viewer", "viewed", "viewed_at")
    search_fields = ("viewer__username", "viewed__username")


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ("id", "from_user", "to_user", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("from_user__username", "to_user__username")
