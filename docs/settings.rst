========
Settings
========

You should specify settings in your settings.py like this::

    WEB3AUTH_USER_ADDRESS_FIELD = 'address'
    WEB3AUTH_USER_SIGNUP_FIELDS = ['email', 'username']


In the above example the following User model is used:

.. code-block:: python

    from django.contrib.auth.models import AbstractUser
    from django.db import models
    from django.utils.translation import ugettext_lazy as _
    from web3auth.utils import validate_eth_address

    class User(AbstractUser):
        address = models.CharField(max_length=42, verbose_name=_("Ethereum wallet address"), unique=True,
                               validators=[validate_eth_address], null=True, blank=True)

        def __str__(self):
            return self.username

Here's a list of available settings:

+--------------------------------+------------+-------------------------------------------------------------------------+
| Setting                        | Default    | Description                                                             |
+================================+============+=========================================================================+
| WEB3AUTH_SIGNUP_ENABLED        | True       | If False, new users won't be able to sign up (used in ``signup_view``)  |
+--------------------------------+------------+-------------------------------------------------------------------------+
| WEB3AUTH_USER_SIGNUP_FIELDS    | ['email']  | Specifies field to be used in signup form for a new User model          |
+--------------------------------+------------+-------------------------------------------------------------------------+
| WEB3AUTH_USER_ADDRESS_FIELD    | 'username' | Field on the User model, which has ethereum address to check against.   |
+--------------------------------+------------+-------------------------------------------------------------------------+
