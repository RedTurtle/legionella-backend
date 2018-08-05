# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from ..settings import models as settings_model


@python_2_unicode_compatible
class Structure(models.Model):
    """ Modello che rappresenta un IMPIANTO.
    Un impianto può essere di diverso tipo:
    - Ingresso
    - Torre
    - Sottocentrale
    e questa cosa la gestiamo con i settings dove ci
    saranno salvati i vari tipi di Impianto possibili.
    """

    class Meta:
        verbose_name = "impianto"
        verbose_name_plural = "impianti"

    label = models.CharField(
        'nome struttura',
        max_length=200)

    struct_type = models.ForeignKey(
        settings_model.Settings,
        null=True,
        blank=True,
        verbose_name='tipo di impianto',
    )

    def __str__(self):
        return self.label
