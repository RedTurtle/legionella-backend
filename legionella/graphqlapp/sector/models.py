# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Sector(models.Model):
    """ Modello che rappresenta un singolo settore dell'ospedale.
    """
    class Meta:
        verbose_name = "settore"
        verbose_name_plural = "settori"

    label = models.CharField(
        'codice',
        max_length=200)

    description = models.CharField(
        'descrizione',
        max_length=200, default="")

    def __str__(self):
        return "Settore " + str(self.label) + " - " + str(self.description)
