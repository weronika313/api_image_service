from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ImageViewSet, ExpiringLinkAPIView

router = DefaultRouter(trailing_slash=False)
router.register(r"images", ImageViewSet, basename="image")


urlpatterns = [
    url(r"^", include(router.urls)),
    path(
        "expiring_image/<link_uuid>",
        ExpiringLinkAPIView.as_view(),
        name="expiring-link",
    ),
]
