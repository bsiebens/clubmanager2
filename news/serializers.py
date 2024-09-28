from bs4 import BeautifulSoup
from django.utils import text
from rest_framework import serializers

from .models import NewsItem


class NewsItemSerializer(serializers.ModelSerializer):
    summary = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    main_picture = serializers.SerializerMethodField()
    pictures = serializers.SerializerMethodField()
    teams = serializers.SerializerMethodField()

    class Meta:
        model = NewsItem
        fields = ["summary", "teams", "content", "main_picture", "pictures", "title", "slug", "publish_on"]

    def get_summary(self, obj: NewsItem) -> str:
        summary = BeautifulSoup(obj.formatted(), "html.parser")

        for img in summary.find_all("img"):
            if len(img.parent.contents) == 1:
                img.parent.decompose()

            else:
                img.decompose()

        return text.Truncator(summary).words(40, html=True)

    def get_content(self, obj: NewsItem) -> str:
        return obj.formatted()

    def get_main_picture(self, obj: NewsItem) -> dict[str, str | int]:
        if obj.main_picture() is not None:
            return {
                "url": obj.main_picture().picture.url,
                "height": obj.main_picture().picture.height,
                "width": obj.main_picture().picture.width,
            }

        return None

    def get_pictures(self, obj: NewsItem) -> list[dict[str, str | int]]:
        return [{"url": picture.picture.url, "height": picture.picture.height, "width": picture.picture.height} for picture in obj.pictures.exclude(main_picture=True).all()]

    def get_teams(self, obj: NewsItem) -> list[str]:
        return [team.short_name for team in obj.teams.all()]
