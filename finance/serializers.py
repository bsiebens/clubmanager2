from rest_framework import serializers

from .models import Sponsor


class SponsorSerializer(serializers.ModelSerializer):
    width = serializers.IntegerField(source="logo.width")
    height = serializers.IntegerField(source="logo.height")

    class Meta:
        model = Sponsor
        fields = ["id", "logo", "name", "url", "width", "height"]
