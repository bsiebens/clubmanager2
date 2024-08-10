from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class NewsItem(models.Model):
    """A news item. This can be both an internal as well as an external message."""

    class StatusChoices(models.IntegerChoices):
        DRAFT = 0
        IN_REVIEW = 1
        RELEASED = 2

    title = models.CharField(_("title"), max_length=250)
    text = models.TextField(_("text"))
    slug = models.SlugField(_("slug"), unique=True)
    author = models.ForeignKey(get_user_model(), verbose_name=_("author"), on_delete=models.PROTECT)
    status = models.IntegerField(_("status"), choices=StatusChoices.choices, default=StatusChoices.DRAFT)
    publish_on = models.DateTimeField(
        _("Publish on"), default=timezone.now, help_text="Date and time on which this item should be published. Only released items will be posted."
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("news item")
        verbose_name_plural = _("news items")
