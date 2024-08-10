import rules
from django.contrib.auth.models import AbstractUser

from .models import NewsItem


@rules.predicate
def is_author(user: AbstractUser | None, news_item: NewsItem | None) -> bool:
    if news_item is not None:
        return user == news_item.author

    return True


@rules.predicate
def is_released(user: AbstractUser | None, news_item: NewsItem | None) -> bool:
    if news_item is not None:
        return news_item.status == NewsItem.StatusChoices.RELEASED

    return False


is_editor = rules.is_group_member("editors")

# Activate rules per model
rules.add_perm("news", rules.always_allow)
rules.add_perm("news.add_newsitem", rules.is_staff)
rules.add_perm("news.view_newsitem", is_author | is_released)
rules.add_perm("news.change_newsitem", is_author | is_editor)
rules.add_perm("news.delete_newsitem", is_author | is_editor)
rules.add_perm("news.release_newsitem", is_editor)
