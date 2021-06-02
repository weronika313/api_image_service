import uuid as uuid
from django.db import models
from rest_framework.reverse import reverse
from django.utils import timezone

from project_apps.images.models import Image


class ExpiringUrlExpired(Exception):
    """Custom exception raised when trying to use an expired link."""
    pass


class ExpiringUrl(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(default=timezone.now())
    expires_at = models.DateTimeField()

    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    @property
    def has_expired(self):
        """Return True if we've gone past the expiry date."""
        return self.expires_at < timezone.now()

    def get_absolute_url(self, request):
        """Returns the reverse() url."""
        return reverse('expiring-link', kwargs={'link_uuid': str(self.uuid)}, request=request)

    def reverse(self, request):
        return self.get_absolute_url(request)

