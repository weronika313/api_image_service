from django.contrib import admin
from .models import Plan, ThumbnailSize

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'has_access_to_org_img', 'can_generate_expiring_links',
                    'display_available_thumbnail_sizes')


@admin.register(ThumbnailSize)
class ThumbnailSizeAdmin(admin.ModelAdmin):
    list_display = ('size',)

