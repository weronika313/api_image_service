from rest_framework import serializers

from project_apps.expiring_url.models import ExpiringUrl


class ExpiringUrlSerializer(serializers.ModelSerializer):
    time_to_expiry = serializers.IntegerField()

    class Meta:
        model = ExpiringUrl
        read_only_fields = ("uuid", "created_at", "expires_at", "image")
        fields = ("uuid", "created_at", "expires_at", "image", "time_to_expiry")

    def validate_time_to_expiry(self, value):
        if value < 300 or value > 30000:
            raise serializers.ValidationError(
                "Time to expiry has to be between 300 and 300000."
            )
        return value
