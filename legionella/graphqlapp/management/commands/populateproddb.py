# -*- coding: utf-8 -*-

from .utils import realdata
from django.conf import settings
from django.core.management.base import BaseCommand
from graphqlapp import logger
import logging


hdlr = logging.FileHandler(settings.LOGGER_FILE_HANDLER)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(hdlr)


class Command(BaseCommand):
    help = """Populate the production db for the Legionella-Backend project
    with a base of real data to get the application started."""

    flush = True

    def handle(self, *args, **options):
        # self.stdout.write(self.style.NOTICE(
        #     "** Populating Legionella Production DB with real data **"))
        logger.info("Excecuting populateproddb")
        realdata.create_floors()
        realdata.create_settingstructtype()
        realdata.create_range()
        realdata.create_structures()
        realdata.create_buildings()
        realdata.create_sectors()
        realdata.create_settinglegionella()
        realdata.create_settingCompany()
        realdata.create_groups()
        realdata.create_users()
        realdata.create_settingmaxfileupload()
        realdata.create_settingallowedfileext()
        realdata.create_settingfieldspermission()
        realdata.create_settingsnotesactions()
        realdata.create_settingrisklevel()
        realdata.create_settingsufclthreshold()
