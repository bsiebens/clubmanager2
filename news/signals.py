from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from news.models import NewsItem, Picture


@receiver(post_save, sender=NewsItem)
@receiver(post_delete, sender=Picture)
@receiver(post_save, sender=Picture)
def update_main_picture(sender, instance, **kwargs) -> None:
    news_object = instance
    if sender == Picture:
        news_object = instance.news_item

    if not news_object.pictures.filter(main_picture=True).exists() and news_object.pictures.count() > 0:
        picture = news_object.pictures.first()
        picture.main_picture = True
        picture.save(update_fields=["main_picture"])
