from django.dispatch import Signal, receiver
from django.db.models.signals import post_delete, post_save, pre_save
from django.contrib.auth.models import Group

from .models import Team, TeamMembership, Season


@receiver(post_delete, sender=Team)
def create_or_update_group(sender, instance, *args, **kwargs):
    try:
        group = Group.objects.get(name=instance.slug)
        group.delete()

    except Group.DoesNotExist:
        pass


@receiver(post_delete, sender=TeamMembership)
def update_group_memberships(sender, instance, *args, **kwargs):
    memberships = TeamMembership.objects.filter(season=Season.get_season(), member=instance.member)
    teams = [membership.team.slug for membership in memberships]

    instance.member.user.groups.set(Group.objects.filter(name__in=teams))
