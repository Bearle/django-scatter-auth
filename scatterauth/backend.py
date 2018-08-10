from django.contrib.auth import get_user_model, backends

from scatterauth.utils import validate_signature, InvalidSignatureException
from scatterauth.settings import app_settings

class ScatterAuthBackend(backends.ModelBackend):
    def authenticate(self, request, pubkey=None, msg=None, signature=None):
        """

        :type signature: str
        """
        # get user model
        User = get_user_model()
        # check if the address the user has provided matches the signature
        try:
            is_valid = validate_signature(msg=msg, sig=signature, pubkey=pubkey)
        except InvalidSignatureException as e:
            return None

        if not is_valid:
            return None
        else:
            # get pubkey field for the user model
                pubkey_field = app_settings.SCATTERAUTH_USER_PUBKEY_FIELD
                kwargs = {
                    pubkey_field+"__iexact": pubkey
                }
                # try to get user with provided data
                user = User.objects.filter(**kwargs).first()
                return user
