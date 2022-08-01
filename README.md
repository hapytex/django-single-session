# Django-single-session

[![PyPi version](https://badgen.net/pypi/v/django-single-session/)](https://pypi.python.org/pypi/django-single-session/)
[![Documentation Status](https://readthedocs.org/projects/django-single-session/badge/?version=latest)](http://django-single-session.readthedocs.io/?badge=latest)
[![PyPi license](https://badgen.net/pypi/license/django-single-session/)](https://pypi.python.org/pypi/django-single-session/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Django app that enforces that a user has only one active session: if the user logs in on another browser/device, then the previous sessions will log out.

The app will also add an extra action to the `ModelAdmin` of the user model (if there is such `ModelAdmin`), that will alow to log out all sessions of a given (set of) user(s).

## Installation

The package can be fetched as `django-single-session`, so for example with `pip` with:

```shell
pip3 install django-single-session
```

One can install the app by adding the `single_session` app to the `INSTALLED_APPS` setting:

```python3
# settings.py

# ...

INSTALLED_APPS = [
    # ...,
    'django.contrib.sessions',
    # ...,
    'single_session'
    # ...
]

MIDDLEWARE = [
    # ...,
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ...,
    'django.contrib.auth.middleware.AuthenticationMiddlware',
    # ...
]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
```

For the `SESSION_ENGINE` setting, the database backend, `django.contrib.sessions.backends.db` should be used, since that is the one where the item is linking to.

In order to work properly, the `SessionMiddleware` and `AuthenticationMiddleware` will be necessary, or another middleware class that will add a `.session` and `.user` attribute on the
request object and will trigger the `user_logged_in` and `user_logged_out` signals with the proper session and user.

and running `migrate` to migrate the database properly:

```shell
python3 manage.py migrate single_session
```

This will by default enforce that a user will only have *one* logged in session. This will *not* proactively logout existing sessions: only if the user logs in with another browser or device,
the old session(s) will be closed.

## Configuration

One can disable the single session behavior by specifying the `SINGLE_USER_SESSION` setting in `settings.py` and thus setting this value to `False` (or any other value with truthiness `False`).

The toolo will also clean up *all* sessions of a user in case that user logs out. This thus means that if a user logs out on one browser/device, they will log out on all other browsers/devices as well. This functionality is still enabled if `SINGLE_USER_SESSION` is set to `False`. You can disable this by setting the `LOGOUT_ALL_SESSION` setting in `settings.py` to `False` (or any other value with truthiness `False`).

## Logging out (other) users

If there is a `ModelAdmin` for the user model (if you use the default user model, then there is such `ModelAdmin`), and the `django.contrib.admin` package is installed,
then that `ModelAdmin` will have extra actions to log out normal users and admin users.

You can thus select users, and log these out with the "*Log out the user on all sessions*" action. This will invalidate all the sessions for (all) the selected user(s). In order to do this,
the `single_session.logout` permission is required, so only admin users and users with such permission can log out other users. Users with such permission can log out users, but
*not* admin users.

There is an extra permission named `single_session.logout_all` to log out all users, including *admin* users. Users with such permission can thus also log out admin users, so it
might be better not to give such permission to all (staff) users.
