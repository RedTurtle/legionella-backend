# -*- coding: utf-8 -*-
from ...settings.service import SettingService
from django.core.management.base import BaseCommand
from graphqlapp import logger


class Command(BaseCommand):

    help = """Set position on risk level that do not have one"""

    def handle(self, *args, **options):
        logger.info("Excecuting fix risk_level position")

        settingService = SettingService()
        settings_list = settingService.getSettingBySettingType('risk_level')
        for i in range(len(settings_list)):
            settings_list[i].position = i
            settings_list[i].save()

        logger.info("Ended excecuting fix risk_level position")
