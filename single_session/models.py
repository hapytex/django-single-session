from django.conf import settings
from django.contrib.sessions.models import Session
from django.db import models
from django.utils.translation import gettext_lazy as _


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

    class Meta:
        permissions = [
            ("logout", _("Logout user sessions in bulk for a given user.")),
            ("logout_all", _("Logout user sessions in bulk for a given (admin) user.")),
        ]
