from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Invitation, Like, Photo, ProfileView
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (InvitationSerializer, LikeSerializer,
                          PhotoSerializer, ProfileViewSerializer)


class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Photo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Like.objects.filter(from_user=self.request.user).select_related(
            "from_user", "to_user"
        )

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)


class ProfileViewViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileViewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProfileView.objects.filter(viewer=self.request.user).select_related(
            "viewer", "viewed"
        )

    def perform_create(self, serializer):
        serializer.save(viewer=self.request.user)


class InvitationViewSet(viewsets.ModelViewSet):
    serializer_class = InvitationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Invitation.objects.filter(from_user=self.request.user).select_related(
            "from_user", "to_user"
        )

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        invitation = self.get_object()
        invitation.status = "accepted"
        invitation.save()
        return Response({"status": "accepted"})

    @action(detail=True, methods=["post"])
    def decline(self, request, pk=None):
        invitation = self.get_object()
        invitation.status = "declined"
        invitation.save()
        return Response({"status": "declined"})
