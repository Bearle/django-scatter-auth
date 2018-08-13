========
Overview
========

Django-scatter-auth features 1 view for login (with JSON responses)
and 2 views for Signup (one with JSON responses, and the other - using Django Forms and rendered templates).

It also has 2 forms, SignupForm (rendered) and LoginForm (uses hidden inputs, used to validate data only).

Possible configuration includes customizable address field (``SCATTERAUTH_USER_PUBKEY_FIELD``), additional fields for User model (``SCATTERAUTH_USER_SIGNUP_FIELDS``),on/off switch for registration (``SCATTERAUTH_SIGNUP_ENABLED``) and domain which will be used for signed message validation (``SCATTERAUTH_DOMAIN``).
You can read more on that in the Settings section.
You should also definitely check example app, it features most of the features needed.

Sign up
-------

The signup process is as follows (signup_view example, signup_api is similar):

1. User heads to the signup URL (``{% url 'scatterauth_signup' %}``)
2. The signup view is rendered with a ``SignupForm`` which includes ``SCATTERAUTH_USER_SIGNUP_FIELDS`` and ``SCATTERAUTH_USER_PUBKEY_FIELD``
3. The user enters required data and clicks the submit button and the POST request fires to the same URL with ``signup_view``
4. Signup view does the following:
    4.1. Creates an instance of a ``SignupForm``.
    4.2. Checks if the registration is enabled.
    4.3. If the registration is closed or form has errors, returns form with errors
    4.4 If the form is valid, saves the user without saving to DB
    4.5. Sets the user public key from the form, saves it to DB
    4.6. Logins the user using ``scatterauth.backend.ScatterAuthBackend``
    4.7. Redirects the user to ``LOGIN_REDIRECT_URL`` or 'next' in get or post params
5. The user is signed up and logged in

Login
-----

The login process is as follows (login_api example):

1. On some page of the website, there is Javascript which gets the user signature for the website's hostname.
2. The signature is sent to the login_api url (``{% url 'scatterauth_login_api' %}``) alongside the public key.
3. The view validates given parameters agains ``LoginForm``
4. The view validates signature with the given public key, and then tries to ``authenticate`` the user
5. If the user is found, the user is signed in and the view responds with a ``redirect_url`` for Javascript to handle
6. If the user is not found, the corresponding error is returned

The Javascript is included in the app, also you can check out example app if you are struggling with logging in the user.
