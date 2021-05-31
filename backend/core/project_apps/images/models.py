from django.db import models, transaction
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from project_apps.users.models import CustomUser as User

from sorl.thumbnail import get_thumbnail
from PIL import Image as pil_image


def user_directory_path(instance, filename):
    return 'images/{0}/'.format(filename)


class Image(models.Model):
    title = models.CharField(max_length=125)
    description = models.CharField(max_length=250, null=True)
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(default=timezone.now())

    owner = models.ForeignKey(User, on_delete=models.PROTECT)


    def get_available_thumbnails_sizes(self):
        user = User.objects.filter(pk=self.owner.id).first()
        available_thumbnail_sizes = user.get_available_thumbnail_sizes()
        return available_thumbnail_sizes

    def make_thumbnail(self, thumbnail_height):
        thumbnail_width = self.get_thumbnail_width(thumbnail_height)
        size = f'{thumbnail_width}x{thumbnail_height}'
        img = get_thumbnail(self.image, size, quality=90)
        Thumbnail.objects.create(thumbnail=img.url, size=size, org_image=self)

    def get_thumbnail_width(self, thumb_height):
        image = pil_image.open(self.image)
        img_width, img_height = image.size
        height_percent = (thumb_height / float(img_height))
        thumb_width = int((float(img_width) * float(height_percent)))

        return thumb_width

    def delete_old_thumbnails(self):
        thumbnails = Thumbnail.objects.filter(org_image=self.pk)
        if thumbnails:
            for thumb in thumbnails:
                thumb.delete()

    def generate_image_thumbnails(self, thumbnail_heights):
        self.delete_old_thumbnails()

        for height in thumbnail_heights:
            self.make_thumbnail(height)

    def get_image_thumbnails(self):
        return Thumbnail.objects.filter(org_image=self.pk)




class Thumbnail(models.Model):
    thumbnail = models.URLField()
    size = models.CharField(max_length=125)

    org_image = models.ForeignKey(Image, on_delete=models.CASCADE)


@receiver(pre_save, sender=User)
@transaction.atomic
def make_new_thumbnails_if_plan_changed(sender, instance, **kwargs):
    try:
        obj = sender.objects.select_for_update().get(pk=instance.pk)
    except sender.DoesNotExist:
        pass
    else:
        if not obj.plan == instance.plan:  # Field has changed
            user_images = Image.objects.filter(owner=obj.pk)
            new_thumb_heights = instance.plan.get_available_thumbnail_sizes_list()

            for image in user_images:

                image.generate_image_thumbnails(new_thumb_heights)

