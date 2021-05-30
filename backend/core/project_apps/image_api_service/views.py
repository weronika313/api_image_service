from django.db import transaction
from rest_framework import viewsets
from project_apps.images.serializers import ImageSerializer
from project_apps.images.models import Image
from rest_framework.exceptions import APIException


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def get_queryset(self):
        user_queryset = self.queryset.filter(owner=self.request.user)
        return user_queryset

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                instance = serializer.save(owner=self.request.user)

        except Exception as e:
            raise APIException(str(e))




