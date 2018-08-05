# -*- coding: utf-8 -*-
from graphqlapp.utils import extract_value_from_input
from .models import Settings as settings_model
from graphql import GraphQLError
from django.core.exceptions import ObjectDoesNotExist
from .service import SettingService

import ast


class SettingsMutationService(object):

    def deleteSetting(self, input):
        settingService = SettingService()

        try:
            settingobj = extract_value_from_input(
                input,
                'setting_id',
                'Settings',
                settings_model)
        except ObjectDoesNotExist:
            raise GraphQLError(
                u'Problemi durante il recupero di alcune impostazioni.'
            )

        settings_list = settingService.getSettingBySettingType('risk_level')
        new_position = settings_list.reverse()[0].position
        settingService.updatePosition(
            old_position=settingobj.position,
            new_position=new_position,
            setting_type=settingobj.setting_type
        )

        return settingobj.delete()

    def updateSetting(self, input):
        try:
            settingobj = extract_value_from_input(
                input,
                'setting_id',
                'Settings',
                settings_model)
        except ObjectDoesNotExist:
            raise GraphQLError(
                u'Problemi durante il recupero di alcune impostazioni.'
            )

        if input.get('setting_id', None):
            if input.get('setting_type', None):
                settingobj.setting_type = input.get('setting_type')
            if input.get('value', None):
                settingobj.value = input.get('value')
            if input.get('description', None):
                settingobj.description = input.get('description')
            if input.get('notes_actions_json', None):
                settingobj.notes_actions_json = ast.literal_eval(
                    input.get('notes_actions_json'))
            # caso in cui venga aggiornata la posizione
            if isinstance(input.get('position'), int):
                settingService = SettingService()
                settingobj.position = settingService.updatePosition(
                    old_position=settingobj.position,
                    new_position=input.get('position'),
                    setting_type=settingobj.setting_type
                )

            settingobj.save()
            return settingobj

    def createSetting(self, input):
        settings = settings_model(
            setting_type=input.get('setting_type'),
            value=input.get('value'),
        )

        if input.get('description', None):
            settings.description = input.get('description')
        if input.get('notes_actions_json', None):
            settings.notes_actions_json = ast.literal_eval(
                input.get('notes_actions_json')
            )
        if settings.setting_type == 'risk_level':
            settingService = SettingService()
            settings_list = settingService.getSettingBySettingType(
                'risk_level'
            )
            settings.position = settings_list.reverse()[0].position + 1

        settings.save()
        return settings
