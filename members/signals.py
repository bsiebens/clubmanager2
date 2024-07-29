import secrets
import string

from django.dispatch import Signal, receiver

new_member_user_created = Signal()


@receiver(new_member_user_created)
def create_and_set_initial_password(sender, *args, **kwargs):
    """Generates a random password and assigns it to the user. To be changed after first login."""
    alphabet = string.ascii_letters + string.digits
    password = "".join(secrets.choice(alphabet) for i in range(20))

    sender.notes = "Initial password: {password}".format(password=password)
    sender.save(updated_fields=["notes"])

    sender.user.set_password(password)
    sender.user.save()
