import datetime

import pytz
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import viewsets, generics, status
from project_apps.images.serializers import ImageSerializer, ExpiringLinkSerializer, ImageSerializerWithOrgImg
from project_apps.expiring_url.serializers import ExpiringUrlSerializer
from project_apps.images.models import Image
from project_apps.expiring_url.models import ExpiringUrl
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from wsgiref.util import FileWrapper
from datetime import timedelta, datetime
from .permissions import UserPermissions, HasAbilityToGenerateExpiringLinks

from rest_framework.reverse import reverse
from sorl.thumbnail import get_thumbnail

from .custom_renderers import JPEGRenderer, PNGRenderer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_queryset = self.queryset.filter(owner=self.request.user)
        return user_queryset

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                print(self.request.user.get_available_thumbnail_sizes())
                instance = serializer.save(owner=self.request.user)

        except Exception as e:
            raise APIException(str(e))

    @action(detail=True, methods=['post'], permission_classes=(HasAbilityToGenerateExpiringLinks,))
    def generate_expiring_link(self, request, pk=None):
        image = self.get_object()
        serializer = ExpiringUrlSerializer(data=request.data)
        if serializer.is_valid():
            expiring_time = serializer.validated_data["time_to_expiry"]
            expires_at = timezone.now() + timedelta(seconds=expiring_time)
            with transaction.atomic():
                expiring_link = ExpiringUrl.objects.create(expires_at=expires_at, image=image)
                url = expiring_link.reverse(request=request)

            data = {'expiring-link': url}

            return Response(data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.request.path.endswith('/generate_expiring_link'):
            return ExpiringUrlSerializer
        elif self.request.user.plan.has_access_to_org_img:
            return ImageSerializerWithOrgImg

        return super(ImageViewSet, self).get_serializer_class()


class ExpiringLinkAPIView(generics.RetrieveAPIView):
    renderer_classes = [PNGRenderer, JPEGRenderer, JSONRenderer]

    def get(self, request, *args, **kwargs):
        expiring_url = ExpiringUrl.objects.get(uuid=self.kwargs['link_uuid'])
        if expiring_url:
            if expiring_url.expires_at > timezone.now():
                image = expiring_url.image.image
                return Response(image, content_type='image/png')
            else:
                return JsonResponse({"error": "link has expired"},
                                status=status.HTTP_410_GONE)
