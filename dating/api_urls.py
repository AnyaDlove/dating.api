from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api_views import (InvitationViewSet, LikeViewSet, PhotoViewSet,
                        ProfileViewViewSet)

router = DefaultRouter()
router.register(r"photos", PhotoViewSet, basename="photo")
router.register(r"likes", LikeViewSet, basename="like")
router.register(r"views", ProfileViewViewSet, basename="view")
router.register(r"invitations", InvitationViewSet, basename="invitation")

urlpatterns = [
    path("", include(router.urls)),
]
