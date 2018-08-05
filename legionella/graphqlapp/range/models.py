# -*- coding: utf-8 -*-

from ..settings import models as settings_model
from datetime import datetime
from django.contrib.postgres.fields import JSONField
from django.db import models


class Range(models.Model):
    """ Modello che rappresenta gli INTERVALLI dei vari livelli di RISCHIO.
    Ogni campo è un JSON salvato sul db.

    Il campo "flag" specifica se il Range è attivo/in uso.
    Può esserci SOLO UN RANGE ATTIVO ALLA VOLTA. Quando ne viene creato uno
    nuovo, quello vecchio va impostato con flag = False.
    """

    class Meta:
        verbose_name = "intervallo di rischio"
        verbose_name_plural = "intervalli di rischio"

    range_type = models.ForeignKey(
        settings_model.Settings,
        null=True,
        blank=True
    )
    cold_temperature = JSONField(default=dict, blank=True)
    cold_flow_temperature = JSONField(default=dict, blank=True)
    hot_temperature = JSONField(default=dict, blank=True)
    hot_flow_temperature = JSONField(default=dict, blank=True)
    ufcl = JSONField(default=dict, blank=True)
    chlorine_dioxide = JSONField(default=dict, blank=True)

    creation_date = models.DateField(
        'data di creazione',
        default=datetime.today,
        blank=True)
    flag = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)
