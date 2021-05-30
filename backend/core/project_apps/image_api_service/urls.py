from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter
from .views import ImageViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'images', ImageViewSet, basename="images")


urlpatterns = [
    url(r"^", include(router.urls)),
]