# -*- coding: utf-8 -*-

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import Group
from graphqlapp.utils import humanize_string


@python_2_unicode_compatible
class Settings(models.Model):
    """ I settaggi generali dell'applicativo.
    Vedi anche la documentazione per maggiori info.

    type: field_permission
    I record con questo tipo servono a specificare quali sono i permessi dei
    singoli field. Bisogna specificare anche l' owner di quel field.

    type: sampling_value
    I settaggi relativi alle diverse soglie/bande di rilevazione della
    legionella (es. <50, <100, >100).

    Il record che ha il flag 'has_legionella_type' settato a True, è il valore
    del rilevamento a cui va associato il ceppo di legionella.

    type: action
    I settaggi delle varie azioni e note per i vari campionamenti.
    """

    class Meta:
        verbose_name = "impostazione"
        verbose_name_plural = "impostazioni"

    setting_type = models.CharField(max_length=50)
    value = models.CharField(max_length=2000)
    int_value = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=150, blank=True)
    position = models.PositiveIntegerField(blank=True, null=True)
    owner = models.ForeignKey(
        Group,
        blank=True,
        null=True
    )

    has_legionella_type = models.NullBooleanField(null=True)

    notes_actions_json = JSONField(default=dict, blank=True)

    def __str__(self):
        return u"{} - {}".format(
            humanize_string(self.setting_type),
            self.value)
