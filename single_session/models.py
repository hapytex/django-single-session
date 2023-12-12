from importlib import import_module

from django.conf import settings
from django.contrib.sessions.models import Session
from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

try:
    if not issubclass(import_module(settings.SESSION_ENGINE).SessionStore,
                      import_module("django.contrib.sessions.backends.db").SessionStore):
        raise ImproperlyConfigured(
            _("The django-single-session package can only work with the 'django.contrib.sessions.backends.db' "
              "or derived backends as SESSION_ENGINE.")
        )
except (ImportError, AttributeError):
    raise ImproperlyConfigured(
        _("The django-single-session package requires a session backend compatible "
          "with 'django.contrib.sessions.backends.db")
    )

if "django.contrib.sessions" not in settings.INSTALLED_APPS:
    raise ImproperlyConfigured(
        _(
            "The django-single-session package can only work if the 'django.contrib.sessions' app is installed in INSTALLED_APPS."
        )
    )


class UserSession(models.Model):
    """
    A model used to store the relation between the session ids and the user model.
    This is used to determine efficiently what session(s) belong to what user.

    The model also defines two extra permissions that can be used to log out all users,
    and all users except the admin users.
    """

    session = models.OneToOneField(
        Session,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="usersessions",
        related_query_name="usersession",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+"
    )

    def __str__(self):
        return f"{self.user.username} - {self.session.session_key}"

    class Meta:
        permissions = [
            ("logout", _("Logout user sessions in bulk for a given user.")),
            ("logout_all", _("Logout user sessions in bulk for a given (admin) user.")),
        ]
