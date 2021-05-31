from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):

    thumbnails = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Image
        read_only_fields = ['owner', 'created_at']
        fields = ['title', 'description', 'image', 'thumbnails', 'created_at', 'owner']

    def get_thumbnails(self, image):
        thumbnails = image.get_image_thumbnails()
        return {f"{thumb.size} px": thumb.thumbnail for thumb in thumbnails}
