# -*- coding: utf-8 -*-
from ..utils import extract_value_from_input
from ..settings.models import Settings as settings_model
from ..range.models import Range as ranges_model
from django.core.exceptions import ObjectDoesNotExist
from graphql import GraphQLError

import ast


class RangeMutationService(object):

    def updateRange(self, input):
        """
        aggiornamento di un range
        input:
            input: dict con i parametri per l'aggiornamento
        output:
            ranges: istanza del modello del range
        """
        try:
            if input.get('range_type', None):
                structure_type = extract_value_from_input(
                    input,
                    'range_type',
                    'Settings',
                    settings_model
                )
        except ObjectDoesNotExist:
            raise GraphQLError(
                u'Problemi durante il recupero di una struttura.'
            )

        # inserisco il nuovo range
        ranges = extract_value_from_input(
            input,
            'range_id',
            'Range',
            ranges_model
        )

        if input.get('ufcl', None):
            ranges.ufcl = ast.literal_eval(input.get('ufcl'))
        if input.get('chlorine_dioxide', None):
            ranges.chlorine_dioxide = ast.literal_eval(
                input.get('chlorine_dioxide'))
        if input.get('cold_temperature', None):
            ranges.cold_temperature = ast.literal_eval(
                input.get('cold_temperature'))
        if input.get('cold_flow_temperature', None):
            ranges.cold_flow_temperature = ast.literal_eval(
                input.get('cold_flow_temperature'))
        if input.get('hot_temperature', None):
            ranges.hot_temperature = ast.literal_eval(
                input.get('hot_temperature'))
        if input.get('hot_flow_temperature', None):
            ranges.hot_flow_temperature = ast.literal_eval(
                input.get('hot_flow_temperature'))
        if input.get('range_type', None):
            ranges.range_type = structure_type

        ranges.save()
        return ranges

    def createRange(self, input):
        """
        creazione di un nuovo range
        input:
            input: dict con i parametri per l'inserimento
        output:
            ranges: istanza del modello dal range
        """
        try:
            structure_type = extract_value_from_input(
                input,
                'range_type',
                'Settings',
                settings_model
            )
        except ObjectDoesNotExist:
            raise GraphQLError(
                u'Problemi durante il recupero di una struttura.'
            )

        # recupero il vecchio range della struttura e lo metto il suo
        # flag a false
        old_active_ranges = ranges_model.objects.get(
            flag=True,
            range_type=structure_type
        )
        if old_active_ranges:
            old_active_ranges.flag = False
            old_active_ranges.save()

        # inserisco il nuovo range
        ranges = ranges_model(
            range_type=structure_type,
        )

        if input.get('ufcl'):
            ranges.ufcl = ast.literal_eval(input.get('ufcl'))
        if input.get('chlorine_dioxide'):
            ranges.chlorine_dioxide = ast.literal_eval(
                input.get('chlorine_dioxide'))
        if input.get('cold_temperature'):
            ranges.cold_temperature = ast.literal_eval(
                input.get('cold_temperature'))
        if input.get('cold_flow_temperature'):
            ranges.cold_flow_temperature = ast.literal_eval(
                input.get('cold_flow_temperature'))
        if input.get('hot_temperature'):
            ranges.hot_temperature = ast.literal_eval(
                input.get('hot_temperature'))
        if input.get('hot_flow_temperature'):
            ranges.hot_flow_temperature = ast.literal_eval(
                input.get('hot_flow_temperature'))

        ranges.save()
        return ranges
