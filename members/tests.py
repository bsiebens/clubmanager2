import re

from django.contrib.auth.hashers import check_password
from django.test import TestCase

from .models import Member


class MemberTest(TestCase):
    def test_member_creation_no_password(self):
        member = Member.create_member(first_name="First Name", last_name="Last Name", email="firstName.lastName@test.com", username="test")

        self.assertIsNotNone(member.user)
        self.assertTrue(member.password_change_required)

    def test_member_creation_with_password(self):
        member = Member.create_member(first_name="First Name", last_name="Last Name", email="firstName.lastName@test.com", username="test", password="TestPassword")

        self.assertIsNotNone(member.user)
        self.assertFalse(member.password_change_required)
        self.assertTrue(check_password("TestPassword", member.user.password))
