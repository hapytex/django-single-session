=====================
Django single session
=====================

django-single-session is a Django library for ensuring that a user can be logged
in to only one session at a time.

**Features:**

   * ensure that a user is logged in at at most one session/browser/device

   * ensure that a user logs out from all sessions if they log out

   * two actions for the `ModelAdmin` to log out (admin) users


.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   getting_started
   admin_actions

.. toctree::
   :maxdepth: 2
   :caption: API documentation

   api_models
   api_signals
   api_admin
   api_apps


.. _`tablib`: https://github.com/jazzband/tablib
