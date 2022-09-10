import pytest
from django.apps import apps
from django.contrib.auth import get_user_model
from django.test import TestCase

from mysite.users.apps import UsersConfig


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username="scott", email="normal@user.com", password="foo")
        self.assertEqual(user.username, "scott")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(username="")
        with self.assertRaises(ValueError):
            User.objects.create_user(username="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser("sophie", "super@user.com", "foo")
        self.assertEqual(admin_user.username, "sophie")
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(username="sophie", email="super@user.com", password="foo", is_superuser=False)


@pytest.mark.django_db
def test_users_app():
    assert UsersConfig.name == "mysite.users"
    assert apps.get_app_config("users").name == "mysite.users"
