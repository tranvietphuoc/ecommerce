from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


User = get_user_model()


class EmailAuthBackend(ModelBackend):
    """
    custom authentication backend to login users using email.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return
        except User.DoesNotExist:
            return

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
