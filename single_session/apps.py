from django.apps import AppConfig
from django.conf import settings


class SingleSessionConfig(AppConfig):
    """
    The app config for the single_session app.
    """

    name = "single_session"
    verbose_name = "Single session"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        """
        This ready() method will load the signals that will be triggered
        if a user has logged in or logged out, and will populate the `ModelAdmin`
        for the user model, given there is such ModelAdmin.
        """
        from single_session import signals  # noqa
        from django.contrib.auth import get_user_model
        from django.contrib.sessions.models import Session

        if "django.contrib.admin" not in settings.INSTALLED_APPS:
            return
        from django.contrib import admin
        from single_session.admin import __actions__, __permissions__

        User = get_user_model()
        UserAdmin = admin.site._registry.get(User)
        if UserAdmin is not None:
            for perm in __permissions__:
                setattr(UserAdmin, perm.__name__, perm)
            user_actions = UserAdmin.actions = list(UserAdmin.actions)
            user_actions += __actions__
