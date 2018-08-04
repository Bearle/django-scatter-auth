========
Overview
========

Django-web3-auth features 1 view for login (with JSON responses)
and 2 views for Signup (one with JSON responses, and the other - using Django Forms and rendered templates).

It also has 2 forms, SignupForm (rendered) and LoginForm (uses hidden inputs, used to validate data only).

Possible configuration includes customizable address field (``WEB3AUTH_USER_ADDRESS_FIELD``), additional fields for User model (``WEB3AUTH_USER_SIGNUP_FIELDS``) and on/off switch for registration (``WEB3AUTH_SIGNUP_ENABLED``).
You can read more on that in the Configuration section.

Sign up
-------

The signup process is as follows (signup_view example, signup_api is similar):

1. User heads to the signup URL (``{% url 'web3auth_signup' %}``)
2. The signup view is rendered with a ``SignupForm`` which includes ``WEB3AUTH_USER_SIGNUP_FIELDS`` and ``WEB3AUTH_USER_ADDRESS_FIELD``
3. The user enters required data and clicks the submit button and the POST request fires to the same URL with ``signup_view``
4. Signup view does the following:
    4.1. Creates an instance of a ``SignupForm``.
    4.2. Checks if the registration is enabled.
    4.3. If the registration is closed or form has errors, returns form with errors
    4.4 If the form is valid, saves the user without saving to DB
    4.5. Sets the user address from the form, saves it to DB
    4.6. Logins the user using ``web3auth.backend.Web3Backend``
    4.7. Redirects the user to ``LOGIN_REDIRECT_URL`` or 'next' in get or post params
5. The user is signed up and logged in

Login
-----

The login process is as follows (login_api example):

1. On some page of the website, there is Javascript which fires a GET request to the ``{% url 'web3auth_login_api' %}``
2. The ``login_api`` view returns 32-char length login token
3. Javascript on the page invites user to sign the token using web3 instance (probably Metamask)
4. If the token is signed, the signature and address are sent ot he same ``login_api`` view
5. The view validates signature & address against ``LoginForm`` to check that the token is signed correctly
6. If the form is valid, the view tries to ``authenticate`` the user with given token,address and signature
7. If the user is found, the user is signed in and the view responds with a ``redirect_url`` for Javascript to handle
8. If the user is not found, the corresponding error is returned


The Javascript is included in the app, also you can check out example app if you are struggling with logging in the user.
