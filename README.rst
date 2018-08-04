=============================
Django-Web3-Auth
=============================

.. image:: https://badge.fury.io/py/django-web3-auth.svg
    :target: https://badge.fury.io/py/django-web3-auth

.. image:: https://travis-ci.org/Bearle/django-web3-auth.svg?branch=master
    :target: https://travis-ci.org/Bearle/django-web3-auth

.. image:: https://codecov.io/gh/Bearle/django-web3-auth/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Bearle/django-web3-auth

django-web3-auth is a pluggable Django app that enables login/signup via an Ethereum wallet (a la CryptoKitties). The user authenticates themselves by digitally signing the session key with their wallet's private key.

.. image:: https://github.com/Bearle/django-web3-auth/blob/master/docs/_static/web3_auth_test.gif?raw=true

Documentation
-------------

The full documentation is at https://django-web3-auth.readthedocs.io.

Example project
---------------

https://github.com/Bearle/django-web3-auth/tree/master/example

You can check out our example project by cloning the repo and heading into example/ directory.
There is a README file for you to check, also.


Features
--------

* Web3 API login, signup
* Web3 Django forms for signup, login
* Checks ethereum address validity
* Uses random token signing as proof of private key posession
* Easy to set up and use (just one click)
* Custom auth backend
* VERY customizable - uses Django settings, allows for custom User model
* Vanilla Javascript helpers included

Quickstart
----------
Install Django-Web3-Auth with pip::

    pip install django-web3-auth

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'web3auth.apps.Web3AuthConfig',
        ...
    )
Set `'web3auth.backend.Web3Backend'` as your authentication backend:

.. code-block:: python

    AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'web3auth.backend.Web3Backend'
    ]
Set your User model's field to use as ETH address provider:

.. code-block:: python

    WEB3AUTH_USER_ADDRESS_FIELD = 'username'

And if you have some other fields you want to be in the SignupForm, add them too:

.. code-block:: python

    WEB3AUTH_USER_SIGNUP_FIELDS = ['email',]


Add Django-Web3-Auth's URL patterns:

.. code-block:: python

    from web3auth import urls as web3auth_urls


    urlpatterns = [
        ...
        url(r'^', include(web3auth_urls)),
        ...
    ]

Add some javascript to handle login:


.. code-block:: html

    <script src="{% static 'web3auth/js/web3auth.js' %}"></script>


.. code-block:: javascript

    function startLogin() {
      if (typeof web3 !== 'undefined') {
        checkWeb3(function (loggedIn) {
          if (!loggedIn) {
            alert("Please unlock your web3 provider (probably, Metamask)")
          } else {
            var login_url = '{% url 'web3auth_login_api' %}';
            web3Login(login_url, console.log, console.log, console.log, console.log, console.log, function (resp) {
              console.log(resp);
              window.location.replace(resp.redirect_url);
            });
          }
        });

      } else {
        alert('web3 missing');
      }
    }

You can access signup using {% url 'web3auth_signup' %}.

If you have any questions left, head to the example app https://github.com/Bearle/django-web3-auth/tree/master/example



Important details and FAQ
-------------------------

1. *If you set a custom address field (WEB3AUTH_USER_ADDRESS_FIELD), it MUST be unique (unique=True).*

This is needed because if it's not, the user can register a new account with the same address as the other one,
meaning that the user can now login as any of those accounts (sometimes being the wrong one).

2. *How do i deal with user passwords or Password is not set*
There should be some code in your project that generates a password using ``User.objects.make_random_password`` and sends it to a user email.
Or, even better, sends them a 'restore password' link.
Also, it's possible to copy signup_view to your project, assign it a url, and add the corresponding lines to set some password for a user.

3. *Why do i have to sign a message? It's not needed in MyEtherWallet or other DApps!*

The main reason is that when using a DApp, you most likely don't have an account on the website, it's accessible only with web3 (Metamask).
When using web3 only to sign into user account, it is necessary to prove your identity with a private key (e.g. sign a random message),
because when we have backend we can't trust any user just by his knowledge of the public address.
Signed message proves that user possesses the private key, associated with the address.


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
