from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ImageViewSet, ThumbnailAPIView

router = DefaultRouter(trailing_slash=False)
router.register(r'images', ImageViewSet, basename="images")


urlpatterns = [
    url(r"^", include(router.urls)),
    path("thumbnail/image_id/<id>", ThumbnailAPIView.as_view())
]