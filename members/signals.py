import secrets
import string

from django.dispatch import Signal, receiver

new_member_user_created = Signal()


@receiver(new_member_user_created)
def create_and_set_initial_password(sender, *args, **kwargs):
    """Generates a random password and assigns it to the user. To be changed after first login."""
    alphabet = string.ascii_letters + string.digits
    password = "".join(secrets.choice(alphabet) for i in range(20))

    if kwargs["password"] is not None:
        password = kwargs["password"]

    sender.password_change_required = kwargs["password"] is None
    sender.save(update_fields=["password_change_required"])

    sender.user.set_password(password)
    sender.user.save()
