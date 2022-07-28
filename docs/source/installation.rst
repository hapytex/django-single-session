============
Installation
============

The package can be fetched as `django-single-session`, so for example with `pip` with:

.. code-block:: console
   
   pip3 install django-single-session


One can install the app by adding the `single_session` app to the `INSTALLED_APPS` setting:

.. code-block:: py3

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

In order to work properly, the `SessionMiddleware` and `AuthenticationMiddleware` will be necessary, or another middleware class that will add a `.session` and `.user` attribute on the
request object and will trigger the `user_logged_in` and `user_logged_out` signals with the proper session and user.

and running `migrate` to migrate the database properly:

.. code-block:: console
   
   python3 manage.py migrate single_session

