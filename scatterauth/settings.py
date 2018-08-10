from django.conf import settings as django_settings


class AppSettings(object):
    @property
    def SCATTERAUTH_USER_PUBKEY_FIELD(self):
        """
        Field on the User model, which has ethereum address to check against.
        This allows you to store it somewhere in arbitrary place other than just username.
        """
        return getattr(django_settings, 'SCATTERAUTH_USER_PUBKEY_FIELD', 'username')

    @property
    def SCATTERAUTH_USER_SIGNUP_FIELDS(self):
        """
        Specifies field to be used in signup form for a new User model
        """
        return getattr(django_settings, "SCATTERAUTH_USER_SIGNUP_FIELDS", ['email'])

    @property
    def SCATTERAUTH_SIGNUP_ENABLED(self):
        """
        Makes it possible to disable signups (similar to allauth)
        """
        return getattr(django_settings, "SCATTERAUTH_SIGNUP_ENABLED", True)

    @property
    def SCATTERAUTH_DOMAIN(self):
        """
        Determines what domain to use for signature verification
        (see https://get-scatter.com/docs/dev/api-authenticate)
        """
        return getattr(django_settings, "SCATTERAUTH_DOMAIN", '')


app_settings = AppSettings()
