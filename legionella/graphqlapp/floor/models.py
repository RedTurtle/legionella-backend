# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Floor(models.Model):
    """ Modello che rappresenta un piano di un edificio.
    """
    class Meta:
        verbose_name = "piano"
        verbose_name_plural = "piani"

    label = models.CharField(
        'codice piano',
        max_length=200)

    def __str__(self):
        return "Piano " + self.label
