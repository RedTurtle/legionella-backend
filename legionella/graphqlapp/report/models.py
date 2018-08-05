# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from ..range import models as range_models
from ..samplerange import models as samplerange_models
from ..settings import models as settings_model
from ..wsp import models as wsp_models


@python_2_unicode_compatible
class Report(models.Model):
    """ Rapporto di campionamento
    Questo modello definisce un rapporto di campionamento generico. Un rapporto
    si specializza poi in freezato o non-freezato """

    class Meta:
        verbose_name = "Rapporto di campionamento"
        verbose_name_plural = "Rapporti di campionamento"

    sample_range = models.ForeignKey(samplerange_models.SampleRange,
                                     on_delete=models.CASCADE)
    wsp = models.ForeignKey(wsp_models.Wsp, on_delete=models.CASCADE)
    risk_level = models.ForeignKey(
        settings_model.Settings,
        verbose_name='Livello di rischio',
        related_name='%(class)s_risk_level',
        null=True,
        blank=True
    )

    # questo campo andrà settato nel momento in cui so a che wsp è relativo
    # il report in modo da sapere in che structure si trova e prendere di
    # conseguenza i range relativi
    rangesettings = models.ForeignKey(range_models.Range,
                                      on_delete=models.CASCADE)
    sampling_date = models.DateField(
        'data del rapporto di campionamento',
        default=datetime.today,
        blank=True,
        null=True)

    # TODO - questo non l'avevamo nella doc. Serve?
    # settings_ref = models.ForeignKey(settings_model.Settings,
    #                                  on_delete=models.CASCADE)

    """ Questo è la parte di Report che è modificabile da un utente Manager.
    """

    cold_ufcl = models.IntegerField(default=0, blank=True, null=True)
    cold_flow_ufcl = models.IntegerField(default=0, blank=True, null=True)
    hot_ufcl = models.IntegerField(default=0, blank=True, null=True)
    hot_flow_ufcl = models.IntegerField(default=0, blank=True, null=True)

    cold_ufcl_type = models.ForeignKey(
        settings_model.Settings,
        related_name='coldufcltype',
        blank=True,
        null=True)
    cold_flow_ufcl_type = models.ForeignKey(
        settings_model.Settings,
        related_name='coldflowufcltype',
        blank=True,
        null=True)
    hot_ufcl_type = models.ForeignKey(
        settings_model.Settings,
        related_name='hotufcltype',
        blank=True,
        null=True)
    hot_flow_ufcl_type = models.ForeignKey(
        settings_model.Settings,
        related_name='howflowufcltype',
        blank=True,
        null=True)

    cold_ufcl_sampling_selection = models.ForeignKey(
        settings_model.Settings,
        related_name='coldufclsamplingselection',
        blank=True,
        null=True)
    cold_flow_ufcl_sampling_selection = models.ForeignKey(
        settings_model.Settings,
        related_name='coldflowufclsamplingselection',
        blank=True,
        null=True)
    hot_ufcl_sampling_selection = models.ForeignKey(
        settings_model.Settings,
        related_name='hotufclsamplingselection',
        blank=True,
        null=True)
    hot_flow_ufcl_sampling_selection = models.ForeignKey(
        settings_model.Settings,
        related_name='hotflowufclsamplingselection',
        blank=True,
        null=True)

    notes_actions = JSONField(default=dict, blank=True, null=True)
    after_sampling_status = JSONField(default=dict, blank=True, null=True)
    review_date = models.DateField(
        blank=True,
        null=True
    )

    """ Questo è la parte di Report che è modificabile da un utente Tecnico.
    """

    # Temperature
    cold_temperature = models.FloatField(default=0, blank=True, null=True)
    cold_flow_temperature = models.FloatField(default=0, blank=True, null=True)
    hot_temperature = models.FloatField(default=0, blank=True, null=True)
    hot_flow_temperature = models.FloatField(default=0, blank=True, null=True)

    # Biossido
    cold_chlorine_dioxide = models.FloatField(default=0, blank=True, null=True)
    cold_flow_chlorine_dioxide = models.FloatField(default=0, blank=True,
                                                   null=True)
    hot_chlorine_dioxide = models.FloatField(default=0, blank=True, null=True)
    hot_flow_chlorine_dioxide = models.FloatField(default=0, blank=True,
                                                  null=True)

    def __str__(self):
        return "Rapporto per il wsp " + self.wsp.code
        + " del " + self.sampling_date.strftime('%d-%m-%y')
