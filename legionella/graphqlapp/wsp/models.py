# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from ..building import models as building_models
from ..floor import models as floor_models
from ..sector import models as sector_models
from ..settings import models as settings_models
from ..structure import models as structure_models

# TODO - scoprire lo scopo di operative_status e obsolence_date e
# cosa cambia nella logica di un WSP (esempio: aggregatedWsps)

from .queryset import MyQuerySet


@python_2_unicode_compatible
class Wsp(models.Model):
    """ Modello che rappresenta un singolo punto di campionamento.
    """
    class Meta:
        verbose_name = "wsp"
        verbose_name_plural = "wsp"
        ordering = ['code']

    objects = MyQuerySet.as_manager()

    code = models.CharField(
        'codice',
        max_length=100)

    old_name = models.CharField(
        'vecchio nome',
        max_length=100,
        default='',
        blank=True)

    structure = models.ForeignKey(
        structure_models.Structure,
        on_delete=models.CASCADE,
        verbose_name='impianto',
    )

    building = models.ForeignKey(
        building_models.Building,
        on_delete=models.CASCADE,
        verbose_name='edificio',
    )

    floor = models.ForeignKey(
        floor_models.Floor,
        on_delete=models.CASCADE,
        verbose_name='piano',
    )

    # livello di rischio del WSP
    risk_level = models.ForeignKey(
        settings_models.Settings,
        related_name='%(class)s_risk_level',
        verbose_name='Livello di rischio',
        default=None,
    )

    # Un WSP può far parte di più di un settore.
    sector = models.ManyToManyField(
        sector_models.Sector,
        verbose_name='settore',
        blank=True,
    )

    description = models.CharField(
        'descrizione',
        max_length=100,
        default='',
        blank=True,
    )

    closed_rooms = models.CharField(
        'stanze chiuse',
        max_length=40,
        default='',
        blank=True,
    )

    open_rooms = models.CharField(
        'stanze aperte',
        max_length=40,
        default='',
        blank=True,
    )

    # ma questo serve? CHECK - TODO
    # adesso lasciato da parte (editable=False, viene nascosto)
    risk_threshold = models.ForeignKey(
        settings_models.Settings,
        verbose_name='Intevalli di rischio',
        related_name='%(class)s_risk_threshold',
        null=True,
        blank=True,
        editable=False,
    )

    start_date = models.DateField(
        'attivo dal',
        default=datetime.today,
        null=True,
        blank=True,
    )

    obsolence_date = models.DateField(
        'disattivo dal',
        default=datetime.today,
        null=True,
        blank=True,
    )

    operative_status = models.BooleanField(
        'operativo',
        default=False)

    # dobbiamo inserire 4 boolean che mi dicono che tipo di prelievi vengono
    # fatti su una certa wsp
    cold = models.NullBooleanField(
        verbose_name='Campionamento Acqua Fredda da fare?',
        default=None)
    cold_flow = models.NullBooleanField(
        verbose_name='Campionamento Acqua Fredda Scorrimento da fare?',
        default=None)
    hot = models.NullBooleanField(
        verbose_name='Campionamento Acqua Calda da fare?',
        default=None)
    hot_flow = models.NullBooleanField(
        verbose_name='Campionamento Acqua Calda Scorrimento da fare?',
        default=None)

    def __str__(self):
        return "Wsp " + self.code
