# -*- coding: utf-8 -*-

from .authentication.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# Estensiamo le classi base dei form di django e modifichiamo solo quello che
# ci interessa in base alle modifiche dell'utente custom che abbiamo fatto.


class CustomUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', )
        error_css_class = 'error'


class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        # del self.fields['username']

    class Meta:
        model = User
        fields = '__all__'
