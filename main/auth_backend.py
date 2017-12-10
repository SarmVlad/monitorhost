from django.contrib.auth.models import User

class EmailAuthBackend(object):

    def authenticate(self, username=None, email=None, password=None):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None

        if not user.check_password(password) and not user.is_active:
            return None

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None