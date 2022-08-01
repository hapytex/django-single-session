=============
Admin actions
=============

If one uses the admin site(s), and there is a `ModelAdmin` for the user model, then the package adds two extra actions to that admin.
These actions can log out (normal) users, and all (including admin) users.

For users to work with these actions, they should be a super user (administrator), or have the `single_session.logout` and `single_session.logout_all`
permissions respectively. We strongly advise *not* to give a user the `single_session.logout_all` permission, since that would mean
that that user can log out administrator users, and by keeping these logged out, thus prevent administrators to do their job properly.
