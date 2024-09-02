import rules
from django.contrib.auth.models import AbstractUser


@rules.predicate
def is_organization_admin(user: AbstractUser | None) -> bool:
    if user is not None:
        return user.member.is_organization_admin

    return False


rules.add_perm("members", is_organization_admin)
