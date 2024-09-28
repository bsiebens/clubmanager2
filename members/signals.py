import secrets
import string

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import Signal, receiver

from teams.tasks import update_group_membership

from .models import Member

new_member_user_created = Signal()


@receiver(new_member_user_created)
def create_and_set_initial_password(sender, *args, **kwargs):
    """Generates a random password and assigns it to the user. To be changed after first login."""

    alphabet = string.ascii_letters + string.digits
    password = "".join(secrets.choice(alphabet) for i in range(20))

    if kwargs["password"] is not None and kwargs["password"] != "":
        password = kwargs["password"]

    sender.password_change_required = kwargs["password"] is None or kwargs["password"] == ""
    if sender.password_change_required:
        sender.notes = "Initial password: {password}".format(password=password)

    sender.save(update_fields=["password_change_required", "notes"])

    sender.user.set_password(password)
    sender.user.save()


@receiver(m2m_changed)
def group_removed(sender, **kwargs):
    instance = kwargs["instance"]
    action = kwargs["action"]

    if isinstance(instance, get_user_model()) and not instance.is_superuser:
        if action == "post_remove":
            if instance.is_staff and not instance.groups.filter(name="admin").exists():
                instance.is_staff = False
                instance.save(update_fields=["is_staff"])

        if action == "post_add":
            if not instance.is_staff and instance.groups.filter(name="admin").exists():
                instance.is_staff = True
                instance.save(update_fields=["is_staff"])


@receiver(post_save, sender=Member)
def update_group_memberships(sender, instance: Member, *args, **kwargs) -> None:
    update_group_membership(instance.user.id)
    # update_group_membership.delay_on_commit(instance.user.id)
