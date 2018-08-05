# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.http import urlquote
from ..settings.models import Settings as settings_model


# controllare se ha fatto l'override dei metodi base dell'utente
class UserManager(BaseUserManager):
    """
    """


class CustomUserManager(BaseUserManager):
    """
    """

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class User(AbstractUser):
    """ Modello dell'utente custom: usiamo la mail come username per fare
    login.
    """

    email = models.EmailField(_('email address'), max_length=254, unique=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        blank=True,
        null=True,
        help_text=_('150 chars or less. Letters, digits and @/./+/-/_ only.'),)

    USERNAME_FIELD = 'email'  # username -> email (required to login)
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_field_perm(self, model, field):

        # recupero i permessi per un certo campo
        field_permission = settings_model.objects.filter(
            value=model + '.' + field)
        if field_permission:
            user_groups = self.groups.all()
            if not field_permission[0].owner in user_groups:
                return False
        return True
