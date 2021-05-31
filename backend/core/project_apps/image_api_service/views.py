import datetime

from django.db import transaction
from rest_framework import viewsets, generics, status
from project_apps.images.serializers import ImageSerializer, ExpiringLinkSerializer, ImageSerializerWithOrgImg
from project_apps.images.models import Image
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
        serializer = ExpiringLinkSerializer(data=request.data)
        if serializer.is_valid():
            expiring_time = datetime.now() + timedelta(seconds=serializer.validated_data["time_to_expiry"])
            print(expiring_time)

            data={'expiring-link': reverse('expiring-link', kwargs={"id": image.id, "expiring_time": expiring_time},
                                           request=request)}

            return Response(data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.request.path.endswith('/generate_expiring_link'):
            return ExpiringLinkSerializer
        elif self.request.user.plan.has_access_to_org_img:
            return ImageSerializerWithOrgImg

        return super(ImageViewSet, self).get_serializer_class()


class ExpiringLinkAPIView(generics.RetrieveAPIView):
    renderer_classes = [PNGRenderer, JPEGRenderer, JSONRenderer]

    def get(self, request, *args, **kwargs):
        date_expiring = datetime.strptime(self.kwargs['expiring_time'][:19], '%Y-%m-%d %H:%M:%S')
        if date_expiring>datetime.now():
            org_img = Image.objects.get(id=self.kwargs['id']).image
            data = org_img

            return Response(data, content_type='image/png')
        else:
            return Response({"error": "link has expired"},
                            status=status.HTTP_404_NOT_FOUND)



