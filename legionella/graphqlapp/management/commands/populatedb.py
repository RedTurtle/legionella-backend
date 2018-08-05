# -*- coding: utf-8 -*-

# from graphqlapp.config import RISK_LEVEL
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone
from django.utils.timezone import utc
from graphqlapp.authentication.models import User
from graphqlapp.range.models import Range
from graphqlapp.settings.models import Settings
from .utils import realdata
from .utils.populate_db_config import CONTENTYPE_PERMISSIONS_FOR_MANAGER
from .utils.samplerange import create_samplerange
from .utils.new_report import create_reports
from .utils.new_wsp import create_wsps
import datetime


class Command(BaseCommand):
    help = """Populate the db for the Legionella-Backend project
    with fake data."""

    flush = True

    def handle(self, *args, **options):
        # self.stdout.write(self.style.NOTICE("** Populating Legionella DB "
        #                                     "with dummy data **"))

        realdata.create_settingsufclthreshold()
        self.create_settingsnotesactions()
        realdata.create_settingrisklevel()
        realdata.create_settingstructtype()
        realdata.create_settinglegionella()
        realdata.create_settingCompany()
        realdata.create_settingmaxfileupload()
        realdata.create_settingallowedfileext()

        realdata.create_floors()
        realdata.create_structures()
        realdata.create_buildings()
        realdata.create_sectors()
        realdata.create_groups()
        realdata.create_users()

        create_samplerange(self)
        create_wsps(self)
        # self.create_range()
        realdata.create_range()
        create_reports(self)

        # Setting the application env for development
        # self.create_groups()
        # self.create_users()

        realdata.create_settingfieldspermission()

        # self.stdout.write(self.style.SUCCESS("** Legionella DB populated "
        #                                      "with dummy data **"))

    # def create_range(self):
    #     """
    #     This functions creates the ranges.
    #     """
    #
    #     if self.flush:
    #         allRanges = Range.objects.all()
    #         for r in allRanges:
    #             r.delete()
    #
    #     r = Range(
    #         creation_date=datetime.datetime.strptime(
    #             '2017-05-16T02:10',
    #             '%Y-%m-%dT%H:%M').replace(
    #             tzinfo=utc),
    #         range_type=Settings.objects.get(
    #             Q(setting_type='struct_type'),
    #             Q(value='torre')
    #         ),
    #         cold_temperature=[
    #             {"from": 0.0, "to": 15.0, "level": 'critical', "priority": 0},
    #             {"from": 15.1, "to": 20.0, "level": 'danger', "priority": 1},
    #             {"from": 20.1, "to": 25.0, "level": 'bad', "priority": 2},
    #             {"from": 25.1, "to": 100.0, "level": 'good', "priority": 3}
    #         ],
    #         cold_flow_temperature=[
    #             {"from": 0.0, "to": 10.0, "level": 'critical', "priority": 0},
    #             {"from": 10.1, "to": 15.0, "level": 'danger', "priority": 1},
    #             {"from": 15.1, "to": 20.0, "level": 'bad', "priority": 2},
    #             {"from": 20.1, "to": 100.0, "level": 'good', "priority": 3}
    #         ],
    #         hot_temperature=[
    #             {"from": 10.0, "to": 15.0, "level": 'critical', "priority": 0},
    #             {"from": 15.1, "to": 20.0, "level": 'danger', "priority": 1},
    #             {"from": 20.1, "to": 60.0, "level": 'bad', "priority": 2},
    #             {"from": 60.1, "to": 100.0, "level": 'good', "priority": 3}
    #         ],
    #         hot_flow_temperature=[
    #             {"from": 20.0, "to": 25.0, "level": 'critical', "priority": 0},
    #             {"from": 25.1, "to": 30.0, "level": 'danger', "priority": 1},
    #             {"from": 30.1, "to": 70.0, "level": 'bad', "priority": 2},
    #             {"from": 70.1, "to": 100.0, "level": 'good', "priority": 3}
    #         ],
    #
    #         ufcl=[
    #             {"from": 0.0, "to": 50.0, "level": 'critical', "priority": 0},
    #             {"from": 50.1, "to": 100.0, "level": 'danger', "priority": 1},
    #             {"from": 100.1, "to": 200.0, "level": 'bad', "priority": 2},
    #             {"from": 200.1, "to": 500.0, "level": 'good', "priority": 3}
    #         ],
    #         chlorine_dioxide=[
    #             {"from": 0.0, "to": 0.25, "level": 'critical', "priority": 0},
    #             {"from": 0.25, "to": 0.50, "level": 'danger', "priority": 1},
    #             {"from": 0.50, "to": 0.75, "level": 'bad', "priority": 2},
    #             {"from": 0.75, "to": 1.0, "level": 'good', "priority": 3}
    #         ],
    #
    #         flag=True
    #     )
    #     r.save()
    #
    #     r = Range(
    #         creation_date=timezone.now(),
    #         range_type=Settings.objects.get(
    #             Q(setting_type='struct_type'),
    #             Q(value='sottocentrale')
    #         ),
    #         cold_temperature=[
    #             {"from": 0.0, "to": 15.0, "level": 'danger', "priority": 0},
    #             {"from": 15.1, "to": 20.0, "level": 'bad', "priority": 1},
    #             {"from": 20.1, "to": 25.0, "level": 'good', "priority": 2},
    #             {"from": 25.1, "to": 100.0, "level": 'perfect', "priority": 3}
    #         ],
    #         cold_flow_temperature=[
    #             {"from": 0.0, "to": 15.0, "level": 'danger', "priority": 0},
    #             {"from": 15.1, "to": 20.0, "level": 'bad', "priority": 1},
    #             {"from": 20.1, "to": 25.0, "level": 'good', "priority": 2},
    #             {"from": 25.1, "to": 100.0, "level": 'perfect', "priority": 3}
    #         ],
    #         hot_temperature=[
    #             {"from": 10.0, "to": 15.0, "level": 'danger', "priority": 0},
    #             {"from": 15.1, "to": 20.0, "level": 'bad', "priority": 1},
    #             {"from": 20.1, "to": 25.0, "level": 'good', "priority": 2},
    #             {"from": 25.1, "to": 100.0, "level": 'perfect', "priority": 3}
    #         ],
    #         hot_flow_temperature=[
    #             {"from": 10.0, "to": 15.0, "level": 'danger', "priority": 0},
    #             {"from": 15.1, "to": 20.0, "level": 'bad', "priority": 1},
    #             {"from": 20.1, "to": 25.0, "level": 'good', "priority": 2},
    #             {"from": 25.1, "to": 100.0, "level": 'perfect', "priority": 3}
    #         ],
    #
    #         ufcl=[
    #             {"from": 0.0, "to": 50.0, "level": 'danger', "priority": 0},
    #             {"from": 50.1, "to": 100.0, "level": 'bad', "priority": 1},
    #             {"from": 100.1, "to": 200.0, "level": 'good', "priority": 2},
    #             {"from": 200.1, "to": 500.0, "level": 'perfect', "priority": 3}
    #         ],
    #         chlorine_dioxide=[
    #             {"from": 0.0, "to": 0.25, "level": 'danger', "priority": 0},
    #             {"from": 0.25, "to": 0.50, "level": 'bad', "priority": 1},
    #             {"from": 0.50, "to": 0.75, "level": 'good', "priority": 2},
    #             {"from": 0.75, "to": 1.0, "level": 'perfect', "priority": 3}
    #         ],
    #
    #         flag=True
    #     )
    #     r.save()
    #
    #     # TODO - questi sono dati finti!
    #     r = Range(
    #         creation_date=timezone.now(),
    #         range_type=Settings.objects.get(
    #             Q(setting_type='struct_type'),
    #             Q(value='ingresso')
    #         ),
    #         cold_temperature=[
    #             {"from": 0.0, "to": 15.0, "level": 'danger', "priority": 0},
    #             {"from": 15.1, "to": 20.0, "level": 'bad', "priority": 1},
    #             {"from": 20.1, "to": 25.0, "level": 'good', "priority": 2},
    #             {"from": 25.1, "to": 100.0, "level": 'perfect', "priority": 3}
    #         ],
    #         cold_flow_temperature=[
    #             {"from": 0.0, "to": 15.0, "level": 'danger', "priority": 0},
    #             {"from": 15.1, "to": 20.0, "level": 'bad', "priority": 1},
    #             {"from": 20.1, "to": 25.0, "level": 'good', "priority": 2},
    #             {"from": 25.1, "to": 100.0, "level": 'perfect', "priority": 3}
    #         ],
    #         hot_temperature=[
    #             {"from": 10.0, "to": 15.0, "level": 'danger', "priority": 0},
    #             {"from": 15.1, "to": 20.0, "level": 'bad', "priority": 1},
    #             {"from": 20.1, "to": 25.0, "level": 'good', "priority": 2},
    #             {"from": 25.1, "to": 100.0, "level": 'perfect', "priority": 3},
    #             {"from": 100.1, "level": 'bad', "priority": 1}
    #         ],
    #         hot_flow_temperature=[
    #             {"from": 10.0, "to": 15.0, "level": 'danger', "priority": 0},
    #             {"from": 15.1, "to": 20.0, "level": 'bad', "priority": 1},
    #             {"from": 20.1, "to": 25.0, "level": 'good', "priority": 2},
    #             {"from": 25.1, "to": 100.0, "level": 'perfect', "priority": 3},
    #             {"from": 100.1, "level": 'bad', "priority": 1}
    #         ],
    #
    #         ufcl=[
    #             {"from": 0.0, "to": 50.0, "level": 'danger', "priority": 0},
    #             {"from": 50.1, "to": 100.0, "level": 'bad', "priority": 1},
    #             {"from": 100.1, "to": 200.0, "level": 'good', "priority": 2},
    #             {"from": 200.1, "to": 500.0, "level": 'perfect', "priority": 3}
    #         ],
    #         chlorine_dioxide=[
    #             {"from": 0.0, "to": 0.25, "level": 'danger', "priority": 0},
    #             {"from": 0.25, "to": 0.50, "level": 'bad', "priority": 1},
    #             {"from": 0.50, "to": 0.75, "level": 'good', "priority": 2},
    #             {"from": 0.75, "to": 1.0, "level": 'perfect', "priority": 3},
    #             {"from": 1.1, "to": 1.5, "level": 'good', "priority": 2},
    #             {"from": 1.6, "to": 2.0, "level": 'bad', "priority": 1},
    #             {"from": 2.1, "to": 2.5, "level": 'danger', "priority": 0},
    #         ],
    #
    #         flag=True
    #     )
    #     r.save()

    def create_settingsnotesactions(self):
        """ Note e azioni di prova.
        """

        if self.flush:
            allSettingsNotesActions = Settings.objects.filter(
                setting_type='noteaction')
            for setting in allSettingsNotesActions:
                setting.delete()

        # preso da esempio dalla documentazione
        json_prova = [{"label": "Chiusura - sezionamento impianto e svuotamento aree assistenziali non utilizzate/ a chiusura estiva prolungata / sottoposte a ristrutturazione"}, {"label": "Installazione temporanea filtri assoluti bagni stanze di degenza (lavandino-doccia per adulti, lavandino-doccia-bidet per pediatria), bagni assistiti e cucinette"}, {"children": ["Acqua calda, 5min./settimana (gioved\u00ec)", "Acqua calda, 15min./settimana", "Acqua calda, 15min./ogni 2settimane", "Acqua calda, 15min./ogni 3settimane", "Acqua calda, 15min./ogni mese", "Acqua calda, mezz'ora/settimana", "Acqua calda, mezz'ora ogni 2 settimane", "Acqua calda, mezz'ora ogni 3 settimane", "Acqua calda, mezz'ora ogni mese"], "label": "Flussaggio di tutti i terminali (compresi i bagni degli operatori e dell'utenza esterna) aree senza filtri"}, {"children": ["Acqua calda, 5min./settimana (gioved\u00ec)", "Acqua calda, 15min./settimana", "Acqua calda, 15min./ogni 2settimane", "Acqua calda, 15min./ogni 3settimane", "Acqua calda, 15min./ogni mese", "Acqua calda, mezz'ora/settimana", "Acqua calda, mezz'ora ogni 2 settimane", "Acqua calda, mezz'ora ogni 3 settimane", "Acqua calda, mezz'ora ogni mese"], "label": "Flussaggio di tutti i terminali (compresi i bagni degli operatori e dell'utenza esterna) aree con filtri"}, {"label": "Disinfezione shock"}]  # noqa

        banda = Settings(setting_type='noteaction',
                         value='Azioni integrative ad hoc',
                         notes_actions_json=json_prova)
        banda.save()

        json_prova = [{"label": "Installazione permanente filtri assoluti ai terminali di bagni stanze di degenza, bagni assistiti e cucinette nelle aree ad alto rischio"}, {"label": "Flussaggio acqua fredda + calda, 1-2min./settimana (luned\u00ec) di TUTTI I TERMINALI non dotati di filtro assoluto di TUTTE LE AREE OSPEDALIERE (sanitarie, tecniche, amministrative), compresi i bagni dell'utenza"}, {"label": "Disincrostazione 1 volta/settimana (mercoled\u00ec) di TUTTI gli aeratori non dotati di filtro"}, {"label": "Disinfezione in continuo (biossido di cloro) con adeguamento-modifica iniezione (mg/l) alle pompe e adeguamento-modifica cloro libero (mg/l) ai terminali"}, {"label": "Adeguamento-modifica temperatura acqua calda ai ricircoli e ai terminali"}]  # noqa

        banda = Settings(setting_type='noteaction',
                         value='Azioni di base',
                         notes_actions_json=json_prova)
        banda.save()

        json_prova = []

        banda = Settings(setting_type='noteaction',
                         value='Schemi di intervento',
                         notes_actions_json=json_prova)
        banda.save()

#
# SETTING THE APPLICATION ENV
#

    def create_groups(self):
        """ This method creates groups
        """

        if self.flush:
            try:
                groupDel = Group.objects.get(name='team')
                groupDel.delete()
            except ObjectDoesNotExist:
                pass

            try:
                groupDel = Group.objects.get(name='manager')
                groupDel.delete()
            except ObjectDoesNotExist:
                pass

            try:
                groupDel = Group.objects.get(name='tecnico')
                groupDel.delete()
            except ObjectDoesNotExist:
                pass

        newgroup = Group(name="manager")
        newgroup.save()
        for objects in CONTENTYPE_PERMISSIONS_FOR_MANAGER:
            content_type = ContentType.objects.get_for_model(objects)
            permlist = Permission.objects.filter(content_type=content_type)
            for per in permlist:
                newgroup.permissions.add(per)

        newgroup = Group(name="tecnico")
        newgroup.save()

    def create_users(self):
        """ This function create two users: admin e Tecnico.
        Only for development.
        You need to call this method directly, right know it calls the
        one in realdata.
        """

        if self.flush:
            admin = User.objects.filter(email='admin@user.it')
            tecnico = User.objects.filter(email='tecnico@tecnico.it')
            if admin:
                admin[0].delete()
            if tecnico:
                tecnico[0].delete()

        admin = User.objects.create_user(email='admin@admin.it',
                                         password='adminpassword')
        admin.save()
        admin.username = 'admin'
        admin.is_staff = True
        admin.groups.add(Group.objects.get(name="manager"))
        admin.save()

        tecnico = User.objects.create_user(email='tecnico@tecnico.it',
                                           password='tecnicopassword')
        tecnico.save()
        tecnico.username = 'tecnico'
        tecnico.is_staff = True
        tecnico.groups.add(Group.objects.get(name="tecnico"))
        tecnico.save()
