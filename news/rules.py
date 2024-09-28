import rules
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from members.rules import is_organization_admin


@rules.predicate
def is_author(user: AbstractUser | None, news_item) -> bool:
    if news_item is not None:
        return user == news_item.author

    return True


@rules.predicate
def is_released(user: AbstractUser | None, news_item) -> bool:
    from .models import NewsItem

    if news_item is not None:
        return news_item.status == NewsItem.StatusChoices.RELEASED and news_item.publish_on <= timezone.now()

    return False


is_editor = rules.is_group_member("editors")
is_admin = rules.is_group_member("admin")

# Activate rules per model
rules.add_perm("news", is_admin)
rules.add_perm("editors", is_organization_admin)
