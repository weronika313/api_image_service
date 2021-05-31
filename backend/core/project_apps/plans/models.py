from django.db import models


class ThumbnailSize(models.Model):
    size = models.IntegerField(default=200)

    def __str__(self):
        return str(self.size) + ' px'


class Plan(models.Model):
    name = models.CharField(max_length=125)
    has_access_to_org_img = models.BooleanField(default=False)
    can_generate_expiring_links = models.BooleanField(default=False)

    available_thumbnail_sizes = models.ManyToManyField(ThumbnailSize)

    def display_available_thumbnail_sizes(self):
        """Create a string for the thumbnail_sizes. This is required to display sizes in Admin."""
        return ', '.join(str(size) for size in self.available_thumbnail_sizes.all()[:3])

    def get_available_thumbnail_sizes_list(self):
        return [th_size.size for th_size in self.available_thumbnail_sizes.all()]

    display_available_thumbnail_sizes.short_description = 'Available thumbnail sizes'

    def __str__(self):
        return self.name
