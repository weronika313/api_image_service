from abc import ABC

from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    thumbnails = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Image
        read_only_fields = ['owner', 'created_at', ]
        fields = ['title', 'description','image', 'thumbnails', 'created_at', 'owner', ]
        extra_kwargs = {
            'image': {'write_only': True}
        }

    def create(self, validated_data):
        image = Image.objects.create(**validated_data)
        available_heights = image.get_available_thumbnails_sizes()
        if available_heights:
            image.generate_image_thumbnails(available_heights)
        return image

    def get_thumbnails(self, image):
        thumbnails = image.get_image_thumbnails()

        return {f"{thumb.size} px": thumb.thumbnail for thumb in thumbnails}


class ImageSerializerWithOrgImg(serializers.ModelSerializer):
    thumbnails = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Image
        read_only_fields = ['owner', 'created_at']
        write_only_fields = ['image']
        fields = ['title', 'description', 'image', 'thumbnails', 'created_at', 'owner']

    def create(self, validated_data):
        image = Image.objects.create(**validated_data)
        available_heights = image.get_available_thumbnails_sizes()
        if available_heights:
            image.generate_image_thumbnails(available_heights)
        return image

    def get_thumbnails(self, image):
        thumbnails = image.get_image_thumbnails()

        return {f"{thumb.size} px": thumb.thumbnail for thumb in thumbnails}


class ExpiringLinkSerializer(serializers.Serializer):
    time_to_expiry = serializers.IntegerField()

    def validate_time_to_expiry(self, value):
        if value < 300 or value > 30000:
            raise serializers.ValidationError('Time to expiry has to be between 300 and 300000.')
        return value
