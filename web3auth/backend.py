from django.contrib.auth import get_user_model, backends

from web3auth.utils import recover_to_addr
from web3auth.settings import app_settings

class Web3Backend(backends.ModelBackend):
    def authenticate(self, request, address=None, token=None, signature=None):
        """

        :type signature: str
        """
        # get user model
        User = get_user_model()
        # check if the address the user has provided matches the signature
        try:
            address_verify = recover_to_addr(token, signature)
        except:
            return None
        if not address == address_verify:
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
