from rest_framework import serializers

from .models import Invitation, Like, Photo, ProfileView


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["id", "image", "is_main", "uploaded_at"]
        read_only_fields = ["uploaded_at"]


class LikeSerializer(serializers.ModelSerializer):
    from_user_username = serializers.CharField(
        source="from_user.username", read_only=True
    )
    to_user_username = serializers.CharField(source="to_user.username", read_only=True)

    class Meta:
        model = Like
        fields = [
            "id",
            "from_user",
            "from_user_username",
            "to_user",
            "to_user_username",
            "kind",
            "created_at",
        ]
        read_only_fields = ["from_user", "created_at"]

    def validate(self, data):
        from_user = self.context["request"].user
        to_user = data["to_user"]
        if Like.objects.filter(from_user=from_user, to_user=to_user).exists():
            raise serializers.ValidationError("Вы уже оценили этого пользователя.")
        return data


class ProfileViewSerializer(serializers.ModelSerializer):
    viewer_username = serializers.CharField(source="viewer.username", read_only=True)
    viewed_username = serializers.CharField(source="viewed.username", read_only=True)

    class Meta:
        model = ProfileView
        fields = [
            "id",
            "viewer",
            "viewer_username",
            "viewed",
            "viewed_username",
            "viewed_at",
        ]
        read_only_fields = ["viewer", "viewed_at"]


class InvitationSerializer(serializers.ModelSerializer):
    from_user_username = serializers.CharField(
        source="from_user.username", read_only=True
    )
    to_user_username = serializers.CharField(source="to_user.username", read_only=True)

    class Meta:
        model = Invitation
        fields = [
            "id",
            "from_user",
            "from_user_username",
            "to_user",
            "to_user_username",
            "message",
            "status",
            "created_at",
        ]
        read_only_fields = ["from_user", "created_at"]
