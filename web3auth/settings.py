from django.conf import settings as django_settings


class AppSettings(object):
    @property
    def WEB3AUTH_USER_ADDRESS_FIELD(self):
        """
        Field on the User model, which has ethereum address to check against.
        This allows you to store it somewhere in arbitrary place other than just username.
        """
        return getattr(django_settings, 'WEB3AUTH_USER_ADDRESS_FIELD', 'username')

    @property
    def WEB3AUTH_USER_SIGNUP_FIELDS(self):
        """
        Specifies field to be used in signup form for a new User model
        """
        return getattr(django_settings, "WEB3AUTH_USER_SIGNUP_FIELDS", ['email'])

    @property
    def WEB3AUTH_SIGNUP_ENABLED(self):
        """
        Makes it possible to disable signups (similar to allauth)
        """
        return getattr(django_settings, "WEB3AUTH_SIGNUP_ENABLED", True)


app_settings = AppSettings()
