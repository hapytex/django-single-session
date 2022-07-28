from django.conf import settings
from django.contrib.auth import user_logged_in, user_logged_out
from django.contrib.sessions.models import Session
from django.dispatch.dispatcher import receiver
from django.test.signals import setting_changed
from single_session.models import UserSession


def remove_other_sessions(sender, user, request, **kwargs):
    """
    A signal handler attached to the user_logged_in signal that will
    create a UserSession that associates the session with the
    user that has logged in. If the SINGLE_USER_SESSION setting
    is enabled (by default), it will remove all the old sessions
    associated to that user.
    """
    # remove other sessions
    if getattr(settings, "SINGLE_USER_SESSION", True):
        remove_all_sessions(sender, user, request, **kwargs)

    # save current session
    request.session.save()

    # create a link from the user to the current session (for later removal)
    UserSession.objects.get_or_create(
        session_id=request.session.session_key, defaults={"user": user}
    )


def remove_all_sessions(sender, user, request, **kwargs):
    """
    A signal handler attached to the user_logged_out signal that will
    remove all sessions associated to that user. This will run if the
    LOGOUT_ALL_SESSIONS setting is enabled.
    """
    # remove other sessions
    if user is not None:
        Session.objects.filter(usersession__user=user).delete()


@receiver(setting_changed)
def change_settings(sender, setting, value, enter, **kwargs):
    """
    A signal handler that is attached to the setting_changed handler
    that will subscribe and unsubscribe the signal handlers to the
    proper signals.
    """
    if setting == "LOGOUT_ALL_SESSIONS":
        if value or not enter:  # teardown: value is None
            user_logged_out.connect(remove_all_sessions)
        else:
            user_logged_out.disconnect(remove_all_sessions)


user_logged_in.connect(remove_other_sessions)
if getattr(settings, "LOGOUT_ALL_SESSIONS", True):
    user_logged_out.connect(remove_all_sessions)
