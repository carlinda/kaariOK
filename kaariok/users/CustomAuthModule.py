from django.conf import settings
from django.contrib.auth.models import User

class CustomBackend:
    """
    Authenticate without a password (used for User selector).
    """
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None