# -*- coding: utf-8 -*-
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
import datetime


@python_2_unicode_compatible
class SampleRange(models.Model):
    """ Modello che rappresenta l'INTERVALLO DI CAMPIONAMENTO.
    """
    class Meta:
        verbose_name = "intervallo di campionamento"
        verbose_name_plural = "intervalli di campionamento"

    dates_list = ArrayField(
        models.DateField(
            default=datetime.date.today,
            null=True,
            blank=True
        ),
    )

    company = models.CharField(max_length=80)
    title = models.CharField(max_length=110)
    description = models.CharField(max_length=200, null=True, blank=True)
    filter_on = models.BooleanField(default=False)

    manager_block = models.BooleanField(default=False)
    final_block = models.BooleanField(default=False)

    tecnico_block = models.BooleanField(default=False)

    freeze_date = models.DateField(default=None, null=True, blank=True)
    reports_freeze = JSONField(default=dict, blank=True)

    def __str__(self):
        return "Intervallo " + str(self.id)

    # esempio lista di date:
    # listadate = [ datetime.date(2017,11,10), datetime.date(2017,11,15)]
    # sr = Samplerange(company="cumpa", title="titolo", dates_list=listadate)
