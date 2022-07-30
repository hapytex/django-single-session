from django.contrib import admin
from django.contrib.sessions.models import Session
from django.utils.translation import gettext_lazy as _


@admin.action(
    description=_("Log out the user on all sessions"),
    permissions=["single_session_logout"],
)
def logout_user_on_all_sessions(modeladmin, request, queryset):
    """
    An action to log out all the users that are not admin users.
    This requires a single_session.logout permission.
    """
    Session.objects.filter(
        usersession__user__in=queryset, usersession__user__is_superuser=False
    ).delete()


@admin.action(
    description=_("Log out the (admin) user on all sessions"),
    permissions=["single_session_logout_all"],
)
def logout_all_users_on_all_sessions(modeladmin, request, queryset):
    """
    An action to log out all the users including admin users.
    This requires a single_session.logout_all permission.
    """
    Session.objects.filter(usersession__user__in=queryset).delete()


def has_single_session_logout_permission(request, instance=None):
    """
    Checks if the user has a single_session.logout permission.
    """
    return request.user.has_perm("single_session.logout")


def has_single_session_logout_all_permission(request, instance=None):
    """
    Checks if the user has a single_session.logout_all permission.
    """
    return request.user.has_perm("single_session.logout_all")


__permissions__ = [
    has_single_session_logout_permission,
    has_single_session_logout_all_permission,
]

__actions__ = [logout_user_on_all_sessions, logout_all_users_on_all_sessions]
