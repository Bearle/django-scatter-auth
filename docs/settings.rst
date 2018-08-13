========
Settings
========

You should specify settings in your settings.py like this::

    SCATTERAUTH_USER_PUBKEY_FIELD = 'pubkey'
    SCATTERAUTH_USER_SIGNUP_FIELDS = ['email', 'username']


In the above example the following User model is used:

.. code-block:: python

    from django.contrib.auth.models import AbstractUser
    from django.db import models
    from django.utils.translation import ugettext_lazy as _

    class User(AbstractUser):
        pubkey = models.CharField(max_length=53, verbose_name=_("Public key"), unique=True, null=True, blank=True)

        def __str__(self):
            return self.username

Here's a list of available settings:

+-----------------------------------+------------+-----------------------------------------------------------------------------------------------+
| Setting                           | Default    | Description                                                                                   |
+===================================+============+===============================================================================================+
| SCATTERAUTH_SIGNUP_ENABLED        | True       | If False, new users won't be able to sign up (used in ``signup_view``)                        |
+-----------------------------------+------------+-----------------------------------------------------------------------------------------------+
| SCATTERAUTH_USER_SIGNUP_FIELDS    | ['email']  | Specifies field to be used in signup form for a new User model                                |
+-----------------------------------+------------+-----------------------------------------------------------------------------------------------+
| SCATTERAUTH_USER_PUBKEY_FIELD     | 'username' | Field on the User model, which has public key to check against.                               |
+-----------------------------------+------------+-----------------------------------------------------------------------------------------------+
| SCATTERAUTH_DOMAIN                | ''         | Determines what domain to use for signature verification. If '' - request.get_host() is used  |
+-----------------------------------+------------+-----------------------------------------------------------------------------------------------+
