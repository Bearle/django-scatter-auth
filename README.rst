=============================
django-scatter-auth
=============================

.. image:: https://badge.fury.io/py/django-scatter-auth.svg
    :target: https://badge.fury.io/py/django-scatter-auth

.. image:: https://travis-ci.org/Bearle/django-scatter-auth.svg?branch=master
    :target: https://travis-ci.org/Bearle/django-scatter-auth

.. image:: https://codecov.io/gh/Bearle/django-scatter-auth/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Bearle/django-scatter-auth

django-scatter-auth is a pluggable Django app that enables login/signup via Scatter (EOS extension wallet). The user authenticates themselves by digitally signing the hostname with their wallet's private key.

.. image:: https://github.com/Bearle/django-scatter-auth/blob/master/docs/_static/django_scatter_auth_test2.gif?raw=true

Documentation
-------------

The full documentation is at https://django-scatter-auth.readthedocs.io.

Example project
---------------

https://github.com/Bearle/django-scatter-auth/tree/master/example

You can check out our example project by cloning the repo and heading into example/ directory.
There is a README file for you to check, also.


Features
--------

* Scatter API login, signup
* Scatter Django forms for signup, login
* Checks signature (validation)
* Uses hostname signing as proof of private key posession
* Easy to set up and use (just one click)
* Custom auth backend
* VERY customizable - uses Django settings, allows for custom User model
* Vanilla Javascript helpers included

Quickstart
----------
Install django-scatter-auth with pip::

    pip install django-scatter-auth

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'scatterauth.apps.scatterauthConfig',
        ...
    )
Set `'scatterauth.backend.ScatterAuthBackend'` as your authentication backend:

.. code-block:: python

    AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'scatterauth.backend.ScatterAuthBackend'
    ]
Set your User model's field to use as public key storage:

.. code-block:: python

    SCATTERAUTH_USER_PUBKEY_FIELD = 'username'

And if you have some other fields you want to be in the SignupForm, add them too:

.. code-block:: python

    SCATTERAUTH_USER_SIGNUP_FIELDS = ['email',]


Add django-scatter-auth's URL patterns:

.. code-block:: python

    from scatterauth import urls as scatterauth_urls


    urlpatterns = [
        ...
        url(r'^', include(scatterauth_urls)),
        ...
    ]

Add some javascript to handle login:


.. code-block:: html

    <script src="{% static 'scatterauth/js/scatterauth.js' %}"></script>


.. code-block:: javascript

    var login_url = '{% url 'scatterauth_login_api' %}';
    document.addEventListener('scatterLoaded', scatterExtension => {
      console.log('scatter loaded');
      if (scatter.identity) {
        console.log("Identity found");
        loginWithAuthenticate(login_url,console.log,console.log,console.log,console.log, function (resp) {
          window.location.replace(resp.redirect_url);
        });
      } else {
        console.log('identity not found, have to signup');
      }
    });

You can access signup using {% url 'scatterauth_signup' %} and API signup using {% url 'scatterauth_signup_api' %}.

If you have any questions left, head to the example app https://github.com/Bearle/django-scatter-auth/tree/master/example



Important details and FAQ
-------------------------

1. *If you set a custom public key field (SCATTERAUTH_USER_PUBKEY_FIELD), it MUST be unique (unique=True).*

This is needed because if it's not, the user can register a new account with the same public key as the other one,
meaning that the user can now login as any of those accounts (sometimes being the wrong one).

2. *How do i deal with user passwords or Password is not set*

There should be some code in your project that generates a password using ``User.objects.make_random_password`` and sends it to a user email.
Or, even better, sends them a 'restore password' link.
Also, it's possible to copy signup_view to your project, assign it a url, and add the corresponding lines to set some password for a user.

3. *Why don't i have to sign a message? It's needed in django-web3-auth, how this app is secure?*

This app uses scatter's ``authenticate`` function to handle message signing - hostname being the signed message.
This means that the user & the client share knowledge of the original message and the server can verify
client's possession of the private key corresponding to the public key.


Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
