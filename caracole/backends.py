from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


# TODO: move this to its own repo


class EmailOrUsernameModelBackend(ModelBackend):
    """
    This backends lets an user authenticate with his username or email
    """
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel._default_manager.get(**{'email' if '@' in username else 'username': username})
            if user.check_password(password):
                return user
        except:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)
