from django.dispatch import Signal, receiver
from django.db.models.signals import post_delete, post_save, pre_save
from django.contrib.auth.models import Group

from .models import Team, TeamMembership, Season
from .tasks import update_group_membership


@receiver(post_save, sender=Team)
def create_or_update_group(sender, instance: Team, *args, **kwargs) -> None:
    if instance.tracker.has_changed("slug"):
        if instance.tracker.previous("slug") is None:
            Group.objects.create(name=instance.slug)

        else:
            group = Group.objects.get(name=instance.tracker.previous("slug"))
            group.name = instance.slug
            group.save(update_fields=["name"])


@receiver(post_delete, sender=Team)
def delete_group(sender, instance: Team, *args, **kwargs):
    try:
        group = Group.objects.get(name=instance.slug)
        group.delete()

    except Group.DoesNotExist:
        pass


@receiver([post_save, post_delete], sender=TeamMembership)
def update_group_memberships(sender, instance: TeamMembership, *args, **kwargs) -> None:
    update_group_membership.delay_on_commit(instance.member.user.id)
