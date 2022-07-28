from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.db.models import Q
from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from single_session.models import UserSession

# Create your tests here.


class SingleSessionTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user1 = User.objects.create_superuser(username="foo", password="foo")
        self.user2 = User.objects.create_superuser(username="bar", password="bar")

    def _pre_setup(self):
        super()._pre_setup()
        self.client2 = Client()
        self.client3 = Client()

    def login_foo(self, client, items=1):
        self.assertTrue(client.login(username="foo", password="foo"))
        self.validate_session_number(items=items)

    def login_bar(self, client, items=1):
        self.assertTrue(client.login(username="bar", password="bar"))
        self.validate_session_number(items=items)

    def logout(self, client, items=0):
        client.logout()
        self.validate_session_number(items=items)

    def validate_session_number(self, items=1):
        self.assertEqual(items, UserSession.objects.count(), UserSession.objects.all())
        self.assertEqual(items, Session.objects.count(), Session.objects.all())

    def test_login_logout_scenario(self):
        self.validate_session_number(0)
        self.login_foo(self.client)
        self.login_foo(self.client2)  # login in new browser, logs out the old one
        self.login_bar(self.client3, 2)
        self.login_foo(self.client, 2)
        self.logout(self.client, 1)
        self.logout(self.client3)

    @override_settings(SINGLE_USER_SESSION=False)
    def test_login_logout_scenario_without_single_session(self):
        self.validate_session_number(0)
        self.login_foo(self.client)
        self.login_foo(self.client2, 2)  # second session for foo
        self.login_bar(self.client3, 3)
        self.login_foo(self.client, 3)  # another login on client1
        self.logout(self.client, 1)  # logs out both sessions
        self.logout(self.client3)

    @override_settings(SINGLE_USER_SESSION=False, LOGOUT_ALL_SESSIONS=False)
    def test_login_logout_scenario_without_logout_all(self):
        self.validate_session_number(0)
        self.login_foo(self.client)
        self.login_foo(self.client2, 2)
        self.login_bar(self.client3, 3)
        self.login_foo(self.client, 3)
        self.logout(self.client, 2)  # logs out only one session
        self.logout(self.client3, 1)
