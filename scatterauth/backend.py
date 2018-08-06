from django.contrib.auth import get_user_model, backends

from scatterauth.utils import validate_signature
from scatterauth.settings import app_settings

class Web3Backend(backends.ModelBackend):
    def authenticate(self, request, address=None, pubkey=None, token=None, signature=None):
        """

        :type signature: str
        """
        # get user model
        User = get_user_model()
        # check if the address the user has provided matches the signature
        if not validate_signature(msg=token, sig=signature, pubkey=pubkey):
            return None
        else:
            # get address field for the user model
                address_field = app_settings.SCATTERAUTH_USER_ADDRESS_FIELD
                kwargs = {
                    address_field+"__iexact": address
                }
                # try to get user with provided data
                user = User.objects.filter(**kwargs).first()
                return user
