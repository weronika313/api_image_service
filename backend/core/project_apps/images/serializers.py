from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        read_only_fields = ['owner', 'created_at']
        fields = ['title', 'description', 'image', 'created_at', 'owner']
