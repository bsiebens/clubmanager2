from django.shortcuts import render
from django.views import View

from django.shortcuts import render
from django.db.models import Q
from .models import Sponsor
from news.models import NewsItem
from django.utils import timezone
import random


def index(request):
    today = timezone.now()

    sponsors = Sponsor.objects.filter(start_date__lte=today.date()).filter(Q(end_date=None) | Q(end_date__gte=today.date()))
    random.shuffle(sponsors)  # Let's give them a shuffle so that they are trully random

    news_items = (
        NewsItem.objects.filter(status=NewsItem.StatusChoices.RELEASED, publish_on__lte=today)
        .exclude(type=NewsItem.NewsItemTypeChoices.INTERNAL)
        .order_by("-publish_on")
        .select_related("teams")
    )

    return render(request, "finance/finance/index.html", {"sponsors": sponsors, "news_items": news_items})
