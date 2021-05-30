from django.db import models
from django.utils import timezone
from project_apps.users.models import CustomUser as User


def user_directory_path(instance, filename):
    return 'images/{0}/'.format(filename)


class Image(models.Model):
    title = models.CharField(max_length=125)
    description = models.CharField(max_length=250, null=True)
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(default=timezone.now())

    owner = models.ForeignKey(User, on_delete=models.PROTECT)
