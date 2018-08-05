# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from graphqlapp.authentication.models import User
from graphqlapp.building.models import Building
from graphqlapp.floor.models import Floor
from graphqlapp.range.models import Range
from graphqlapp.sector.models import Sector
from graphqlapp.settings.models import Settings
from graphqlapp.structure.models import Structure
from .populate_db_config import SECTORS, SUBSTATIONS_BUILDINGS, \
    LEGIONELLA_TYPES, CONTENTYPE_PERMISSIONS_FOR_MANAGER, ALLOWED_FILE_EXT, \
    CONTENTYPE_PERMISSIONS_FOR_TECNICO, MANAGER_CANNOT_DELETE
from django.conf import settings
from graphqlapp import logger
import datetime
import logging


hdlr = logging.FileHandler(settings.LOGGER_FILE_HANDLER)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(hdlr)


def create_floors():
    """ This function creates the floors.
    Default floors are 5 in total: from -1 to 3.
    """

    allFloors = Floor.objects.all()
    for floor in allFloors:
        floor.delete()

    piano = Floor(label="-1")
    piano.save()

    piano = Floor(label="0")
    piano.save()

    piano = Floor(label="1")
    piano.save()

    piano = Floor(label="2")
    piano.save()

    piano = Floor(label="3")
    piano.save()


def create_structures():
    """ This function creates structures.

    Default = 6 sottocentrale + 2 torre + 1 ingresso
    """

    allStructures = Structure.objects.all()
    for struct in allStructures:
        struct.delete()

    for i in range(6):
        num = i + 1
        struttura = Structure(
            label="Sottocentrale %d" % num,
            struct_type=Settings.objects.get(
                Q(setting_type='struct_type'),
                Q(value='sottocentrale')
            )
        )
        struttura.save()

    struttura = Structure(
        label="Torre di raffreddamento 1",
        struct_type=Settings.objects.get(
            Q(setting_type='struct_type'),
            Q(value='torre')
        )
    )
    struttura.save()

    struttura = Structure(
        label="Torre di raffreddamento 2",
        struct_type=Settings.objects.get(
            Q(setting_type='struct_type'),
            Q(value='torre')
        )
    )
    struttura.save()

    struttura = Structure(
        label="Ingresso 1",
        struct_type=Settings.objects.get(
            Q(setting_type='struct_type'),
            Q(value='ingresso')
        )
    )
    struttura.save()

    struttura = Structure(
        label="Ingresso 2",
        struct_type=Settings.objects.get(
            Q(setting_type='struct_type'),
            Q(value='ingresso')
        )
    )
    struttura.save()


def create_buildings():
    """ This function creates buildings related tu substations.
    The creation for this instances is related to the configuration in the
    file populate_db_config.py.

    This are data gathered from the excel files so we assume they are
    correct.
    """

    allBuildings = Building.objects.all()
    for build in allBuildings:
        build.delete()

    allStructures = Structure.objects.all()
    for sub in allStructures:
        sub_buildings = SUBSTATIONS_BUILDINGS.get(sub.label)
        if sub_buildings:
            for buildcode in sub_buildings:
                b = Building(label=buildcode, structure=sub)
                b.save()


def create_sectors():
    """ This function creates some sectors based on real data.
    The sectors can be configured in config.py, list SECTORS.
    """
    allSectors = Sector.objects.all()
    for sector in allSectors:
        sector.delete()

    for sector in SECTORS:
        settore = Sector(label=sector[0],
                         description=sector[1])
        settore.save()


def create_settingmaxfileupload():
    """
    setting_type: max_upload_size
    value e int value devono contenere lo stesso valore.
    """
    allSettingStructType = Settings.objects.filter(
        setting_type='max_upload_size')
    for struct_type in allSettingStructType:
        struct_type.delete()

    maxsize = Settings(
        setting_type='max_upload_size',
        int_value=20971520,
        value='20971520',
        description='Dimensione massima upload allegati (in byte)'
    )
    maxsize.save()


def create_settingallowedfileext():
    """
    setting_type: allowed_file_ext
    value e int value devono contenere lo stesso valore.
    """
    allSettingStructType = Settings.objects.filter(
        setting_type='allowed_file_ext')
    for struct_type in allSettingStructType:
        struct_type.delete()

    for extension in ALLOWED_FILE_EXT:
        maxsize = Settings(
            setting_type='allowed_file_ext',
            value=extension,
            description='Estensione accettata in upload di un file.'
        )
        maxsize.save()


def create_settingstructtype():
    """
    struct_type
    Definisce i vari tipi di strutture che formano l'impianto.
    (Ingresso, Torre, Sottocentrale)
    """

    allSettingStructType = Settings.objects.filter(
        setting_type='struct_type')
    for struct_type in allSettingStructType:
        struct_type.delete()

    banda = Settings(
        setting_type='struct_type',
        value='torre',
        description='Torri'
    )
    banda.save()

    banda = Settings(
        setting_type='struct_type',
        value='sottocentrale',
        description='Sottocentrali'
    )
    banda.save()

    banda = Settings(
        setting_type='struct_type',
        value='ingresso',
        description='Ingressi'
    )
    banda.save()


def create_settinglegionella():
    """
    Settings: definiscono i vari ceppi di legionella.
    Qui ce ne sono alcuni presi da dati reali.
    """

    allSettingLegionella = Settings.objects.filter(
        setting_type='legionella'
    )
    for setting in allSettingLegionella:
        setting.delete()

    c = 0
    for ceppo in LEGIONELLA_TYPES:
        tipo = Settings(
            setting_type='legionella',
            value=ceppo[0],
            description=ceppo[1],
            position=c
        )
        tipo.save()
        c += 1


def create_settingCompany():
    """
    Settings che definiscono le possibili aziende/company che fanno i
    campionamenti.
    """

    allSettingLegionella = Settings.objects.filter(
        setting_type='company'
    )
    for setting in allSettingLegionella:
        setting.delete()

    company = Settings(
        setting_type='company',
        value="COMPANY1",
        description="Company 1",
    )
    company.save()


def create_groups():
    """ This method creates the groups for the application.
    """

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
        if objects in MANAGER_CANNOT_DELETE:
            # Rimuovo il permesso di delete per determinati modelli
            permlist = permlist.exclude(
                codename=MANAGER_CANNOT_DELETE[objects])
        for per in permlist:
            newgroup.permissions.add(per)

    newgroup = Group(name="tecnico")
    newgroup.save()

    for objects in CONTENTYPE_PERMISSIONS_FOR_TECNICO:
        content_type = ContentType.objects.get_for_model(objects)
        permlist = Permission.objects.filter(content_type=content_type)
        for per in permlist:
            newgroup.permissions.add(per)


def create_users():
    """ This function create two users: admin e Tecnico.
    """

    admin = User.objects.filter(email='admin@admin.it')
    tecnico = User.objects.filter(email='tecnico@tecnico.it')
    if admin:
        admin[0].delete()
    if tecnico:
        tecnico[0].delete()

    admin = User.objects.create_user(email='admin@admin.it',
                                     password='adminpassword')
    admin.save()
    admin.username = 'admin'
    admin.first_name = 'admin'
    admin.last_name = 'admin'
    admin.is_staff = True
    admin.groups.add(Group.objects.get(name="manager"))
    admin.save()

    tecnico = User.objects.create_user(email='tecnico@tecnico.it',
                                       password='tecnicopassword')
    tecnico.save()
    tecnico.username = 'tecnico'
    tecnico.is_staff = False
    tecnico.groups.add(Group.objects.get(name="tecnico"))
    tecnico.save()


def create_settingfieldspermission():
    """
    This function initialize fields permission for report and samplerange
    """

    allSettingsFieldsPerm = Settings.objects.filter(
        setting_type='field_permission'
    )
    for setting in allSettingsFieldsPerm:
        setting.delete()

    # REPORT #

    # MANAGER

    # UFCL
    permesso = Settings(
        setting_type='field_permission',
        value='Report.cold_ufcl',
        owner=Group.objects.get(name='manager')
    )
    permesso.save()

    permesso = Settings(
        setting_type='field_permission',
        value='Report.cold_flow_ufcl',
        owner=Group.objects.get(name='manager')
    )
    permesso.save()

    permesso = Settings(
        setting_type='field_permission',
        value='Report.hot_ufcl',
        owner=Group.objects.get(name='manager')
    )
    permesso.save()

    permesso = Settings(
        setting_type='field_permission',
        value='Report.hot_flow_ufcl',
        owner=Group.objects.get(name='manager')
    )
    permesso.save()

    # UFCL type
    permesso = Settings(
        setting_type='field_permission',
        value='Report.cold_ufcl_type',
        owner=Group.objects.get(name='manager')
    )
    permesso.save()

    permesso = Settings(
        setting_type='field_permission',
        value='Report.cold_flow_ufcl_type',
        owner=Group.objects.get(name='manager')
    )
    permesso.save()

    permesso = Settings(
        setting_type='field_permission',
        value='Report.hot_ufcl_type',
        owner=Group.objects.get(name='manager')
    )
    permesso.save()

    permesso = Settings(
        setting_type='field_permission',
        value='Report.hot_flow_ufcl_type',
        owner=Group.objects.get(name='manager')
    )
    permesso.save()

    # UFCL Sampling Selections
    permesso = Settings(
        setting_type='field_permission',
        value='Report.cold_ufcl_sampling_selection',
        owner=Group.objects.get(name='manager')
    )
    permesso.save()

    permesso = Settings(
        setting_type='field_permission',
        value='Report.cold_flow_ufcl_sampling_selection',
        owner=Group.objects.get(name='manager')
    )
    permesso.save()

    permesso = Settings(
        setting_type='field_permission',
        value='Report.hot_ufcl_sampling_selection',
        owner=Group.objects.get(name='manager')
    )
    permesso.save()

    permesso = Settings(
        setting_type='field_permission',
        value='Report.hot_flow_ufcl_sampling_selection',
        owner=Group.objects.get(name='manager')
    )
    permesso.save()

    # note e actions
    permesso = Settings(
        setting_type='field_permission',
        value='Report.notes_actions',
        owner=Group.objects.get(name='manager')
    )
    permesso.save()

    # after sampling status
    permesso = Settings(
        setting_type='field_permission',
        value='Report.notes_actions',
        owner=Group.objects.get(name='manager')
    )
    permesso.save()

    # review_date
    permesso = Settings(
        setting_type='field_permission',
        value='Report.review_date',
        owner=Group.objects.get(name='manager')
    )
    permesso.save()

    # TECNICO #

    # TEMPERATURE
    permesso = Settings(
        setting_type='field_permission',
        value='Report.cold_temperature',
        owner=Group.objects.get(name='tecnico')
    )
    permesso.save()

    permesso = Settings(
        setting_type='field_permission',
        value='Report.cold_flow_temperature',
        owner=Group.objects.get(name='tecnico')
    )
    permesso.save()

    permesso = Settings(
        setting_type='field_permission',
        value='Report.hot_temperature',
        owner=Group.objects.get(name='tecnico')
    )
    permesso.save()

    permesso = Settings(
        setting_type='field_permission',
        value='Report.hot_flow_temperature',
        owner=Group.objects.get(name='tecnico')
    )
    permesso.save()

    # BIOSSIDO
    permesso = Settings(
        setting_type='field_permission',
        value='Report.cold_chlorine_dioxide',
        owner=Group.objects.get(name='tecnico')
    )
    permesso.save()

    permesso = Settings(
        setting_type='field_permission',
        value='Report.cold_flow_chlorine_dioxide',
        owner=Group.objects.get(name='tecnico')
    )
    permesso.save()

    permesso = Settings(
        setting_type='field_permission',
        value='Report.hot_chlorine_dioxide',
        owner=Group.objects.get(name='tecnico')
    )
    permesso.save()

    permesso = Settings(
        setting_type='field_permission',
        value='Report.hot_flow_chlorine_dioxide',
        owner=Group.objects.get(name='tecnico')
    )
    permesso.save()

    # SAMPLERANGE #
    # MANAGER
    permesso = Settings(
        setting_type='field_permission',
        value='SampleRange.final_block',
        owner=Group.objects.get(name='manager')
    )
    permesso.save()
    permesso = Settings(
        setting_type='field_permission',
        value='SampleRange.manager_block',
        owner=Group.objects.get(name='manager')
    )
    permesso.save()
    # TECNICO
    permesso = Settings(
        setting_type='field_permission',
        value='SampleRange.tecnico_block',
        owner=Group.objects.get(name='tecnico')
    )
    permesso.save()


def create_settingsnotesactions():
    """ Note e azioni.
    Di base sono "inventate". Prese dai documenti di admin.
    """

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


def create_settingrisklevel():
    """
    This function creates some risk_level settings.
    """

    allSettingRiskTh = Settings.objects.filter(
        setting_type='risk_level')
    for setting in allSettingRiskTh:
        setting.delete()

    banda = Settings(
        setting_type='risk_level',
        value='basso',
        description='Basso'
    )
    banda.save()

    banda = Settings(
        setting_type='risk_level',
        value='medio',
        description='Aumentato'
    )
    banda.save()

    banda = Settings(
        setting_type='risk_level',
        value='alto',
        description='Molto elevato'
    )
    banda.save()


def create_range():
    """
    This functions creates the ranges.
    """

    allRanges = Range.objects.all()
    for r in allRanges:
        r.delete()

    r = Range(
        creation_date=datetime.date(2017, 1, 1),
        range_type=Settings.objects.get(
            Q(setting_type='struct_type'),
            Q(value='torre')
        ),
        cold_temperature=[
            {"from": 24.0, "to": 100.0, "level": 'critical', "priority": 0},
            {"from": 21.0, "to": 23.9, "level": 'danger', "priority": 1},
            {"from": 20.0, "to": 20.9, "level": 'bad', "priority": 2},
            {"from": 0.0, "to": 19.9, "level": 'good', "priority": 3}
        ],
        cold_flow_temperature=[
            {"from": 24.0, "to": 100.0, "level": 'critical', "priority": 0},
            {"from": 21.0, "to": 23.9, "level": 'danger', "priority": 1},
            {"from": 20.0, "to": 20.9, "level": 'bad', "priority": 2},
            {"from": 0.0, "to": 19.9, "level": 'good', "priority": 3}
        ],
        hot_temperature=[
            {"from": 54.0, "to": 120, "level": 'critical', "priority": 0},
            {"from": 0.0, "to": 39.9, "level": 'danger', "priority": 1},
            {"from": 40.0, "to": 47.8, "level": 'bad', "priority": 2},
            {"from": 51.0, "to": 53.9, "level": 'good', "priority": 3},
            {"from": 48.0, "to": 50.9, "level": 'perfect', "priority": 4},
        ],
        hot_flow_temperature=[
            {"from": 54.0, "to": 120, "level": 'critical', "priority": 0},
            {"from": 0.0, "to": 39.9, "level": 'danger', "priority": 1},
            {"from": 40.0, "to": 47.8, "level": 'bad', "priority": 2},
            {"from": 51.0, "to": 53.9, "level": 'good', "priority": 3},
            {"from": 48.0, "to": 50.9, "level": 'perfect', "priority": 4},
        ],

        ufcl=[
            {"from": 100000.1, "level": 'critical', "priority": 0},
            {"from": 10001, "to": 100000, "level": 'danger', "priority": 1},
            {"from": 1001, "to": 10000, "level": 'bad', "priority": 2},
            {"from": 100, "to": 1000, "level": 'good', "priority": 3}
        ],
        chlorine_dioxide=[
            {"to": 0.1, "level": 'bad', "priority": 2},
            {"from": 0.11, "to": 0.3, "level": 'good', "priority": 3},
            {"from": 0.31, "to": 0.5, "level": 'perfect', "priority": 4},
            {"from": 0.51, "to": 1.0, "level": 'good', "priority": 3},
            {"from": 1.01, "level": 'bad', "priority": 2},
        ],

        flag=True
    )
    r.save()

    r = Range(
        creation_date=datetime.date(2017, 1, 2),
        range_type=Settings.objects.get(
            Q(setting_type='struct_type'),
            Q(value='sottocentrale')
        ),
        cold_temperature=[
            {"from": 24.0, "to": 100.0, "level": 'danger', "priority": 0},
            {"from": 21.0, "to": 23.9, "level": 'bad', "priority": 1},
            {"from": 20.0, "to": 20.9, "level": 'good', "priority": 2},
            {"from": 0.0, "to": 19.9, "level": 'perfect', "priority": 3}
        ],
        cold_flow_temperature=[
            {"from": 24.0, "to": 100.0, "level": 'danger', "priority": 0},
            {"from": 21.0, "to": 23.9, "level": 'bad', "priority": 1},
            {"from": 20.0, "to": 20.9, "level": 'good', "priority": 2},
            {"from": 0.0, "to": 19.9, "level": 'perfect', "priority": 3}
        ],
        hot_temperature=[
            {"from": 54.0, "to": 120, "level": 'critical', "priority": 0},
            {"from": 0.0, "to": 39.9, "level": 'danger', "priority": 1},
            {"from": 40.0, "to": 47.8, "level": 'bad', "priority": 2},
            {"from": 51.0, "to": 53.9, "level": 'good', "priority": 3},
            {"from": 48.0, "to": 50.9, "level": 'perfect', "priority": 4},
        ],
        hot_flow_temperature=[
            {"from": 54.0, "to": 120, "level": 'critical', "priority": 0},
            {"from": 0.0, "to": 39.9, "level": 'danger', "priority": 1},
            {"from": 40.0, "to": 47.8, "level": 'bad', "priority": 2},
            {"from": 51.0, "to": 53.9, "level": 'good', "priority": 3},
            {"from": 48.0, "to": 50.9, "level": 'perfect', "priority": 4},
        ],

        ufcl=[
            {"from": 10000.1, "level": 'danger', "priority": 0},
            {"from": 1001.0, "to": 10000.0, "level": 'bad', "priority": 1},
            {"from": 101.0, "to": 1000.0, "level": 'good', "priority": 2},
            {"from": 0.0, "to": 100.0, "level": 'perfect', "priority": 3}
        ],
        chlorine_dioxide=[
            {"to": 0.1, "level": 'bad', "priority": 2},
            {"from": 0.11, "to": 0.3, "level": 'good', "priority": 3},
            {"from": 0.31, "to": 0.5, "level": 'perfect', "priority": 4},
            {"from": 0.51, "to": 1.0, "level": 'good', "priority": 3},
            {"from": 1.01, "level": 'bad', "priority": 2},
        ],

        flag=True
    )
    r.save()

    # TODO - questi sono dati finti!
    r = Range(
        creation_date=datetime.date(2017, 1, 3),
        range_type=Settings.objects.get(
            Q(setting_type='struct_type'),
            Q(value='ingresso')
        ),
        cold_temperature=[
            {"from": 24.0, "to": 100.0, "level": 'danger', "priority": 0},
            {"from": 21.0, "to": 23.9, "level": 'bad', "priority": 1},
            {"from": 20.0, "to": 20.9, "level": 'good', "priority": 2},
            {"from": 0.0, "to": 19.9, "level": 'perfect', "priority": 3}
        ],
        cold_flow_temperature=[
            {"from": 24.0, "to": 100.0, "level": 'danger', "priority": 0},
            {"from": 21.0, "to": 23.9, "level": 'bad', "priority": 1},
            {"from": 20.0, "to": 20.9, "level": 'good', "priority": 2},
            {"from": 0.0, "to": 19.9, "level": 'perfect', "priority": 3}
        ],
        hot_temperature=[
            {"from": 54.0, "to": 120, "level": 'critical', "priority": 0},
            {"from": 0.0, "to": 39.9, "level": 'danger', "priority": 1},
            {"from": 40.0, "to": 47.8, "level": 'bad', "priority": 2},
            {"from": 51.0, "to": 53.9, "level": 'good', "priority": 3},
            {"from": 48.0, "to": 50.9, "level": 'perfect', "priority": 4},
        ],
        hot_flow_temperature=[
            {"from": 54.0, "to": 120, "level": 'critical', "priority": 0},
            {"from": 0.0, "to": 39.9, "level": 'danger', "priority": 1},
            {"from": 40.0, "to": 47.8, "level": 'bad', "priority": 2},
            {"from": 51.0, "to": 53.9, "level": 'good', "priority": 3},
            {"from": 48.0, "to": 50.9, "level": 'perfect', "priority": 4},
        ],

        ufcl=[
            {"from": 10000.1, "level": 'danger', "priority": 0},
            {"from": 1001.0, "to": 10000.0, "level": 'bad', "priority": 1},
            {"from": 101.0, "to": 1000.0, "level": 'good', "priority": 2},
            {"from": 0.0, "to": 100.0, "level": 'perfect', "priority": 3}
        ],
        chlorine_dioxide=[
            {"to": 0.1, "level": 'bad', "priority": 2},
            {"from": 0.11, "to": 0.3, "level": 'good', "priority": 3},
            {"from": 0.31, "to": 0.5, "level": 'perfect', "priority": 4},
            {"from": 0.51, "to": 1.0, "level": 'good', "priority": 3},
            {"from": 1.01, "level": 'bad', "priority": 2},
        ],

        flag=True
    )
    r.save()


def create_settingsufclthreshold():
    """ This functions creates some ufcl threshold bands.
    These are the ones with <50, <100, etc...
    Who has the flag set to true, has the legionella type sampled.
    """

    allSettingsUfclTh = Settings.objects.filter(
        setting_type='sampling_value')
    for setting in allSettingsUfclTh:
        setting.delete()

    banda = Settings(
        setting_type='sampling_value',
        value='≤ 50',
        int_value=49,
        has_legionella_type=False
    )
    banda.save()

    banda = Settings(
        setting_type='sampling_value',
        value='≤ 100',
        int_value=99,
        has_legionella_type=False
    )
    banda.save()

    banda = Settings(
        setting_type='sampling_value',
        value='> 100',
        has_legionella_type=True
    )
    banda.save()
