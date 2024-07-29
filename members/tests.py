import re

from django.contrib.auth.hashers import check_password
from django.test import TestCase

from .models import Member


class MemberTest(TestCase):
    def test_member_creation(self):
        member = Member.obejcts.create(first_name="First Name", last_name="Last Name", email="firstName.lastName@test.com")

        self.assertIsNotNone(member.user)

        password = re.match(r"^Initial password: ([a-zA-Z0-9]+)$", member.notes).groups()[0]
        self.assertTrue(check_password(password, member.user.password))
