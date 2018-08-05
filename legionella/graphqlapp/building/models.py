# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from graphqlapp.structure.models import Structure


@python_2_unicode_compatible
class Building(models.Model):
    """ Modello Edificio
    """
    class Meta:
        verbose_name = "edificio"
        verbose_name_plural = "edifici"

    label = models.CharField(
        'codice edificio',
        max_length=200)

    structure = models.ForeignKey(
        Structure,
        on_delete=models.CASCADE,
        verbose_name='struttura',
    )

    def __str__(self):
        return "Edificio " + str(self.label)
