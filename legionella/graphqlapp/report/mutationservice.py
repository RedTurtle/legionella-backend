# -*- coding: utf-8 -*-

from ..config import MEASURE_TYPE
from ..range.service import RangeService
from ..samplerange.models import SampleRange as samplerange_model
from ..settings.models import Settings as settings_model
from ..settings.service import SettingService
from ..wsp.models import Wsp as wsp_model
from .models import Report as report_model
from .service import ReportService
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from graphql import GraphQLError
from graphqlapp import logger
from graphqlapp.utils import extract_value_from_input
from graphqlapp.utils import humanize_string

import ast
import datetime
import logging

hdlr = logging.FileHandler(settings.LOGGER_FILE_HANDLER)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(hdlr)


class ReportMutationService(object):

    def _samevalue_report_wsp(self, wsp, input):
        if not wsp.cold:
            for value in MEASURE_TYPE['cold']:
                if value in input:
                    raise Exception('cold', value)
        if not wsp.cold_flow:
            for value in MEASURE_TYPE['cold_flow']:
                if value in input:
                    raise Exception('cold_flow', value)
        if not wsp.hot:
            for value in MEASURE_TYPE['hot']:
                if value in input:
                    raise Exception('hot', value)
        if not wsp.hot_flow:
            for value in MEASURE_TYPE['hot_flow']:
                if value in input:
                    raise Exception('hot_flow', value)

    def _validateReportValue(self, setting, value, value_name):
        """
        controlla se il valore di un prelievo di un report si trova all'interno
        del suo range
        input:
            setting: dict che indica i vari range
            value: valore che devo validare
        output:
            boolean che mi indica se il valore è all'interno di un range
        """
        reportService = ReportService()
        if not reportService.alertLevelCalculation(
            setting=setting,
            value=value
        ):
            raise GraphQLError(u"Il valore di " + humanize_string(value_name)
                               + " non rientra in nessuno degli intervalli"
                               u" di rischio.")

    def deleteReport(self, input):
        try:
            reportobj = extract_value_from_input(
                input=input,
                field_id='report_id',
                model_type='Report',
                model=report_model
            )
        except ObjectDoesNotExist:
            raise GraphQLError(
                u'Problemi con il recupero di un rapporto di campionamento.'
            )

        if reportobj.sample_range.manager_block or \
            reportobj.sample_range.tecnico_block or \
                reportobj.sample_range.final_block:
            raise GraphQLError(u"Non si può cancellare un rapporto se il suo "
                               u"intervallo ha almeno una validazione!")

        return reportobj.delete()

    def updateReport(self, input, user_groups):
        # service
        reportService = ReportService()
        settingService = SettingService()
        rangeService = RangeService()

        # CAMPI CON ID
        fields = [
            ('report_id', 'Report', report_model),
            ('wsp', 'Wsp', wsp_model),
            ('sample_range', 'SampleRange', samplerange_model),
            ('cold_ufcl_type', 'Settings', settings_model),
            ('cold_flow_ufcl_type', 'Settings', settings_model),
            ('cold_ufcl_sampling_selection', 'Settings', settings_model),
            ('cold_flow_ufcl_sampling_selection', 'Settings', settings_model),
            ('hot_ufcl_type', 'Settings', settings_model),
            ('hot_flow_ufcl_type', 'Settings', settings_model),
            ('hot_ufcl_sampling_selection', 'Settings', settings_model),
            ('hot_flow_ufcl_sampling_selection', 'Settings', settings_model)
        ]

        fields_with_ids = {}
        try:
            fields_with_ids = {x[0]: extract_value_from_input(
                input=input,
                field_id=x[0],
                model_type=x[1],
                model=x[2]) for x in fields}
        except ObjectDoesNotExist as err:
            raise GraphQLError(
                u'Problemi durante il recupero di alcuni dati.'
            )

        # CONTROLLI LOGICA BLOCCHI
        # user_group = info.context.user.groups.all()
        sample_range = fields_with_ids.get('sample_range')
        if sample_range:
            if sample_range.final_block:
                raise GraphQLError('Il report è già congelato.')
        else:
            raise GraphQLError('Manca l\'intervallo di campionamento.')

        # controllo che il wsp del report sia uguale a quello passato per
        # l'aggiornamento
        if fields_with_ids.get('wsp') != fields_with_ids.get('report_id').wsp:
            # se non è uguale allora controllo che quello nuovo non abbia già
            # un report in questo wsp
            # controllo se già presente un report per un wsp nel samplerange
            param = {}
            param['sample_range'] = fields_with_ids.get('sample_range')
            param['wsp'] = fields_with_ids.get('wsp')

            if reportService.getReportListByDict(param):
                return GraphQLError(
                    u'Questo WSP ha già un report assegnato in questo ' +
                    u'intervallo di campionamento.'
                )

        # controllo se è stato messo un blocco parziale, nel caso in cui sia
        # stato messo allora non deve essere possibile modificare i campi block
        # recupero i campi manager_block e tecnico_block
        param = {}
        param['setting_type'] = "field_permission"
        param['value__contains'] = 'Report.'
        param['owner__in'] = user_groups

        fields_with_permission = settingService.getSettingListByDict(param)

        # Nota: Manager può modificare il campo delle Note/Azioni anche se
        # sono stati applicati entrambi i blocchi
        if sample_range.manager_block:
            # controllo che all'interno dell'input ci siano campi bloccati
            for field in fields_with_permission:
                field_name = field.value.split('Report.', 1)[1]
                if field_name in input \
                   and field.owner.name != 'tecnico' \
                   and field_name != u'notes_actions' \
                   and sample_range.tecnico_block:
                    logger.error(
                        u"Tentata modifica campo {} con "
                        u"lock attivi sul sample range ID: {}".format(
                            humanize_string(field.value),
                            sample_range.id))
                    raise GraphQLError(
                        u"Non è possibile modificare il rapporto di "
                        u"campionamento perchè è già stato validato.")
        if sample_range.tecnico_block:
            # controllo che all'interno dell'input ci siano campi bloccati
            for field in fields_with_permission:
                if field.value.split('Report.', 1)[1] in input \
                   and field.owner.name != 'manager' \
                   and sample_range.manager_block:
                    logger.error(
                        u"Tentata modifica campo {} con "
                        u"lock attivi sul sample range ID: {}".format(
                            field.value,
                            sample_range.id))
                    raise GraphQLError(
                        u"Non è possibile modificare il rapporto di "
                        u"campionamento perchè è già stato validato.")

        # RANGE SETTINGS - info dal WSP e dal tipo di struttura associata.
        # La logica è: i range che sono per il tipo di struttura specificato
        # nei settings e che sono attivi.
        rangesettings = None
        if fields_with_ids.get('wsp'):
            wsp = fields_with_ids.get('wsp')
            wspstruct = wsp.structure.struct_type.value

            # controllo che il report vada ad inserire solo
            # i valori permessi dal wsp
            try:
                self._samevalue_report_wsp(wsp, input)
            except Exception as err:
                raise GraphQLError(
                    u'Questo report non accetta prelievi per il campo {0} '
                    u'perchè il WSP a lui associato non accetta prelievi per '
                    u'questo tipo di misurazioni {1}.'.format(
                        humanize_string(err.args[1]),
                        humanize_string(err.args[0])),
                )

            param = {}
            param['range_type__setting_type'] = 'struct_type'
            param['range_type__value'] = wspstruct
            param['flag'] = True

            rangeobj = rangeService.getRangeListByDict(param)
            if not rangeobj:
                raise GraphQLError(
                    u"Non c'è un range corretto utilizzabile per questo "
                    u"tipo di struttura: {}".format(wspstruct))
            elif len(rangeobj) > 1:
                raise GraphQLError(
                    u"Ci sono troppi range attivi per questo tipo di "
                    u"struttura! {} ."
                    u"Correggi disattivando i vecchi range.".format(
                        wspstruct))

            rangesettings = rangeobj[0]
        else:
            # non ci puo essere un report senza wsp associato
            pass

        sampling_date = None
        if 'sampling_date' in input.keys():
            sampling_date = datetime.datetime.strptime(
                input['sampling_date'],
                "%Y-%m-%d").date()

        review_date = None

        if 'review_date' in input.keys() and input['review_date']:
            review_date = datetime.datetime.strptime(
                input['review_date'],
                "%Y-%m-%d").date()

        # VALORI DI LEGIONELLA
        cold_ufcl = None
        if fields_with_ids.get('cold_ufcl_sampling_selection'):
            if fields_with_ids.get('cold_ufcl_sampling_selection').has_legionella_type:  # noqa
                cold_ufcl = input.get('cold_ufcl', 0)
            else:
                cold_ufcl = fields_with_ids.get(
                    'cold_ufcl_sampling_selection').int_value
            self._validateReportValue(
                setting=rangesettings.ufcl,
                value=cold_ufcl,
                value_name='cold_ufcl',
            )
        cold_flow_ufcl = None
        if fields_with_ids.get('cold_flow_ufcl_sampling_selection'):
            if fields_with_ids.get('cold_flow_ufcl_sampling_selection').has_legionella_type:  # noqa
                cold_flow_ufcl = input.get('cold_flow_ufcl', 0)
            else:
                cold_flow_ufcl = fields_with_ids.get(
                    'cold_flow_ufcl_sampling_selection').int_value
            self._validateReportValue(
                setting=rangesettings.ufcl,
                value=cold_flow_ufcl,
                value_name='cold_flow_ufcl',
            )
        hot_ufcl = None
        if fields_with_ids.get('hot_ufcl_sampling_selection'):
            if fields_with_ids.get('hot_ufcl_sampling_selection').has_legionella_type:  # noqa
                hot_ufcl = input.get('hot_ufcl', 0)
            else:
                hot_ufcl = fields_with_ids.get(
                    'hot_ufcl_sampling_selection').int_value
            self._validateReportValue(
                setting=rangesettings.ufcl,
                value=hot_ufcl,
                value_name='hot_ufcl',
            )
        hot_flow_ufcl = None
        if fields_with_ids.get('hot_flow_ufcl_sampling_selection'):
            if fields_with_ids.get('hot_flow_ufcl_sampling_selection').has_legionella_type:  # noqa
                hot_flow_ufcl = input.get('hot_flow_ufcl', 0)
            else:
                hot_flow_ufcl = fields_with_ids.get(
                    'hot_flow_ufcl_sampling_selection').int_value
            self._validateReportValue(
                setting=rangesettings.ufcl,
                value=hot_flow_ufcl,
                value_name='hot_flow_ufcl',
            )

        # VALORI DI BIOSSIDO
        cold_chlorine_dioxide = None
        if 'cold_chlorine_dioxide' in input.keys():
            cold_chlorine_dioxide = input['cold_chlorine_dioxide']
            if cold_chlorine_dioxide:
                self._validateReportValue(
                    setting=rangesettings.chlorine_dioxide,
                    value=cold_chlorine_dioxide,
                    value_name='cold_chlorine_dioxide',
                )
        cold_flow_chlorine_dioxide = None
        if 'cold_flow_chlorine_dioxide' in input.keys():
            cold_flow_chlorine_dioxide = input['cold_flow_chlorine_dioxide']
            if cold_flow_chlorine_dioxide:
                self._validateReportValue(
                    setting=rangesettings.chlorine_dioxide,
                    value=cold_flow_chlorine_dioxide,
                    value_name='cold_flow_chlorine_dioxide',
                )
        hot_chlorine_dioxide = None
        if 'hot_chlorine_dioxide' in input.keys():
            hot_chlorine_dioxide = input['hot_chlorine_dioxide']
            if hot_chlorine_dioxide:
                self._validateReportValue(
                    setting=rangesettings.chlorine_dioxide,
                    value=hot_chlorine_dioxide,
                    value_name='hot_chlorine_dioxide',
                )
        hot_flow_chlorine_dioxide = None
        if 'hot_flow_chlorine_dioxide' in input.keys():
            hot_flow_chlorine_dioxide = input['hot_flow_chlorine_dioxide']
            if hot_flow_chlorine_dioxide:
                self._validateReportValue(
                    setting=rangesettings.chlorine_dioxide,
                    value=hot_flow_chlorine_dioxide,
                    value_name='hot_flow_chlorine_dioxide',
                )

        # VALORI DI TEMPERATURA
        cold_temperature = None
        if 'cold_temperature' in input.keys():
            cold_temperature = input['cold_temperature']
            if cold_temperature:
                self._validateReportValue(
                    setting=rangesettings.cold_temperature,
                    value=cold_temperature,
                    value_name='cold_temperature',
                )
        cold_flow_temperature = None
        if 'cold_flow_temperature' in input.keys():
            cold_flow_temperature = input['cold_flow_temperature']
            if cold_flow_temperature:
                self._validateReportValue(
                    setting=rangesettings.cold_flow_temperature,
                    value=cold_flow_temperature,
                    value_name='cold_flow_temperature',
                )
        hot_temperature = None
        if 'hot_temperature' in input.keys():
            hot_temperature = input['hot_temperature']
            if hot_temperature:
                self._validateReportValue(
                    setting=rangesettings.hot_temperature,
                    value=hot_temperature,
                    value_name='hot_temperature',
                )
        hot_flow_temperature = None
        if 'hot_flow_temperature' in input.keys():
            hot_flow_temperature = input['hot_flow_temperature']
            if hot_flow_temperature:
                self._validateReportValue(
                    setting=rangesettings.hot_flow_temperature,
                    value=hot_flow_temperature,
                    value_name='hot_flow_temperature',
                )

        if fields_with_ids.get('report_id'):

            report = fields_with_ids.get('report_id')

            if sample_range:
                report.sample_range = sample_range
            if fields_with_ids.get('wsp'):
                report.wsp = fields_with_ids.get('wsp')
                report.risk_level = fields_with_ids.get('wsp').risk_level
            report.rangesettings = rangesettings
            if sampling_date:
                report.sampling_date = sampling_date
            if review_date:
                report.review_date = review_date

            if cold_ufcl:
                report.cold_ufcl = cold_ufcl
            if cold_flow_ufcl:
                report.cold_flow_ufcl = cold_flow_ufcl
            if hot_ufcl:
                report.hot_ufcl = hot_ufcl
            if hot_flow_ufcl:
                report.hot_flow_ufcl = hot_flow_ufcl

            if cold_temperature:
                report.cold_temperature = cold_temperature
            if cold_flow_temperature:
                report.cold_flow_temperature = cold_flow_temperature
            if hot_temperature:
                report.hot_temperature = hot_temperature
            if hot_flow_temperature:
                report.hot_flow_temperature = hot_flow_temperature

            if cold_chlorine_dioxide:
                report.cold_chlorine_dioxide = cold_chlorine_dioxide
            if cold_flow_chlorine_dioxide:
                report.cold_flow_chlorine_dioxide = cold_flow_chlorine_dioxide
            if hot_chlorine_dioxide:
                report.hot_chlorine_dioxide = hot_chlorine_dioxide
            if hot_flow_chlorine_dioxide:
                report.hot_flow_chlorine_dioxide = hot_flow_chlorine_dioxide

            if fields_with_ids.get('cold_ufcl_type'):
                report.cold_ufcl_type = fields_with_ids.get('cold_ufcl_type')
            if fields_with_ids.get('cold_flow_ufcl_type'):
                report.cold_flow_ufcl_type = fields_with_ids.get(
                    'cold_flow_ufcl_type')
            if fields_with_ids.get('hot_ufcl_type'):
                report.hot_ufcl_type = fields_with_ids.get('hot_ufcl_type')
            if fields_with_ids.get('hot_flow_ufcl_type'):
                report.hot_flow_ufcl_type = fields_with_ids.get(
                    'hot_flow_ufcl_type')

            if fields_with_ids.get('cold_ufcl_sampling_selection'):
                report.cold_ufcl_sampling_selection = fields_with_ids.get(
                    'cold_ufcl_sampling_selection')
            if fields_with_ids.get('cold_flow_ufcl_sampling_selection'):
                report.cold_flow_ufcl_sampling_selection = fields_with_ids.get(
                    'cold_flow_ufcl_sampling_selection')
            if fields_with_ids.get('hot_ufcl_sampling_selection'):
                report.hot_ufcl_sampling_selection = fields_with_ids.get(
                    'hot_ufcl_sampling_selection')
            if fields_with_ids.get('hot_flow_ufcl_sampling_selection'):
                report.hot_flow_ufcl_sampling_selection = fields_with_ids.get(
                    'hot_flow_ufcl_sampling_selection')

            if 'notes_actions' in input.keys():
                report.notes_actions = ast.literal_eval(input['notes_actions'])
            if 'after_sampling_status' in input.keys():
                report.after_sampling_status = ast.literal_eval(
                    input['after_sampling_status'])

            report.save()
            return report

    def createReport(self, input):
        reportService = ReportService()
        rangeService = RangeService()

        # CAMPI CON ID (foreign key)
        fields = [
            ('wsp', 'Wsp', wsp_model),
            ('sample_range', 'SampleRange', samplerange_model),
            ('cold_ufcl_type', 'Settings', settings_model),
            ('cold_flow_ufcl_type', 'Settings', settings_model),
            ('cold_ufcl_sampling_selection', 'Settings', settings_model),
            ('cold_flow_ufcl_sampling_selection', 'Settings', settings_model),
            ('hot_ufcl_type', 'Settings', settings_model),
            ('hot_flow_ufcl_type', 'Settings', settings_model),
            ('hot_ufcl_sampling_selection', 'Settings', settings_model),
            ('hot_flow_ufcl_sampling_selection', 'Settings', settings_model)
        ]

        fields_with_ids = None
        try:
            fields_with_ids = {x[0]: extract_value_from_input(
                input=input,
                field_id=x[0],
                model_type=x[1],
                model=x[2]) for x in fields}
        except ObjectDoesNotExist as err:
            raise GraphQLError(
                u'Problemi durante il recupero di alcuni oggetti.'
            )

        # controllo se già presente un report per un wsp in quel samplerange
        param = {}
        param['sample_range'] = fields_with_ids.get('sample_range')
        param['wsp'] = fields_with_ids.get('wsp')

        if reportService.getReportListByDict(param):
            return GraphQLError(
                u'Esiste già un report di questo Wsp per questo '
                u'intervallo di campionamento',
            )

        # controllo che il samplerange a cui voglio assegnare il report
        # non abbia nemmeno un blocco attivato
        if fields_with_ids.get('sample_range').manager_block or \
            fields_with_ids.get('sample_range').tecnico_block or \
                fields_with_ids.get('sample_range').final_block:
            return GraphQLError(
                u'Non è possibile aggiungere un report ad un intervallo ' +
                u'di campionamento che è già stato bloccato o ' +
                u'parzialmente bloccato.'
            )

        # RANGE SETTINGS - info dal WSP e dal tipo di struttura associata.
        # La logica è: i range che sono per il tipo di struttura specificato
        # nei settings e che sono attivi.
        rangesettings = None
        if fields_with_ids.get('wsp'):
            wsp = fields_with_ids.get('wsp')
            wspstruct = wsp.structure.struct_type.value

            # controllo che il report vada ad inserire solo
            # i valori permessi dal wsp
            try:
                self._samevalue_report_wsp(wsp, input)
            except Exception as err:
                raise GraphQLError(
                    u'Questo report non accetta prelievi per il campo {0} '
                    u'perchè il WSP a lui associato non accetta prelievi '
                    u'per questo tipo di misurazioni {1}.'.format(
                        err.args[1], err.args[0])
                )

            param = {}
            param['range_type__setting_type'] = 'struct_type'
            param['range_type__value'] = wspstruct
            param['flag'] = True

            rangeobj = rangeService.getRangeListByDict(param)
            if not rangeobj:
                raise GraphQLError(
                    u"Non ce un range corretto attivabile per un questo "
                    u"tipo di struttura: {}".format(wspstruct))
            elif len(rangeobj) > 1:
                raise GraphQLError(
                    u"Ci sono troppi range attivi per questo tipo "
                    u"di struttura! {} ."
                    u"Correggi disattivando i vecchi range.".format(
                        wspstruct))

            rangesettings = rangeobj[0]

        sampling_date = None
        if input.get('sampling_date', None):
            sampling_date = datetime.datetime.strptime(
                input['sampling_date'],
                "%Y-%m-%d").date()

        review_date = None
        if input.get('review_date', None):
            review_date = datetime.datetime.strptime(
                input['review_date'],
                "%Y-%m-%d").date()

        notes_actions = None
        if input.get('notes_actions', None):
            notes_actions = ast.literal_eval(
                input['notes_actions']
            )

        after_sampling_status = None
        if input.get('after_sampling_status', None):
            after_sampling_status = ast.literal_eval(
                input['after_sampling_status']
            )

        # VALORI DI LEGIONELLA
        cold_ufcl = None
        if fields_with_ids.get('cold_ufcl_sampling_selection'):
            if fields_with_ids.get('cold_ufcl_sampling_selection').has_legionella_type:  # noqa
                cold_ufcl = input.get('cold_ufcl', 0)
            else:
                cold_ufcl = fields_with_ids.get(
                    'cold_ufcl_sampling_selection').int_value
            self._validateReportValue(
                setting=rangesettings.ufcl,
                value=cold_ufcl,
                value_name='cold_ufcl',
            )
        cold_flow_ufcl = None
        if fields_with_ids.get('cold_flow_ufcl_sampling_selection'):
            if fields_with_ids.get('cold_flow_ufcl_sampling_selection').has_legionella_type:  # noqa
                cold_flow_ufcl = input.get('cold_flow_ufcl', 0)
            else:
                cold_flow_ufcl = fields_with_ids.get(
                    'cold_flow_ufcl_sampling_selection').int_value
            self._validateReportValue(
                setting=rangesettings.ufcl,
                value=cold_flow_ufcl,
                value_name='cold_flow_ufcl',
            )
        hot_ufcl = None
        if fields_with_ids.get('hot_ufcl_sampling_selection'):
            if fields_with_ids.get('hot_ufcl_sampling_selection').has_legionella_type:  # noqa
                hot_ufcl = input.get('hot_ufcl', 0)
            else:
                hot_ufcl = fields_with_ids.get(
                    'hot_ufcl_sampling_selection').int_value
            self._validateReportValue(
                setting=rangesettings.ufcl,
                value=hot_ufcl,
                value_name='hot_ufcl',
            )
        hot_flow_ufcl = None
        if fields_with_ids.get('hot_flow_ufcl_sampling_selection'):
            if fields_with_ids.get('hot_flow_ufcl_sampling_selection').has_legionella_type:  # noqa
                hot_flow_ufcl = input.get('hot_flow_ufcl', 0)
            else:
                hot_flow_ufcl = fields_with_ids.get(
                    'hot_flow_ufcl_sampling_selection').int_value
            self._validateReportValue(
                setting=rangesettings.ufcl,
                value=hot_flow_ufcl,
                value_name='hot_flow_ufcl',
            )

        # VALORI DI BIOSSIDO
        cold_chlorine_dioxide = input.get('cold_chlorine_dioxide', None)
        if cold_chlorine_dioxide:
            self._validateReportValue(
                setting=rangesettings.chlorine_dioxide,
                value=cold_chlorine_dioxide,
                value_name='cold_chlorine_dioxide',
            )
        cold_flow_chlorine_dioxide = input.get(
            'cold_flow_chlorine_dioxide', None)
        if cold_flow_chlorine_dioxide:
            self._validateReportValue(
                setting=rangesettings.chlorine_dioxide,
                value=cold_flow_chlorine_dioxide,
                value_name='cold_flow_chlorine_dioxide',
            )
        hot_chlorine_dioxide = input.get('hot_chlorine_dioxide', None)
        if hot_chlorine_dioxide:
            self._validateReportValue(
                setting=rangesettings.chlorine_dioxide,
                value=hot_chlorine_dioxide,
                value_name='hot_chlorine_dioxide',
            )
        hot_flow_chlorine_dioxide = input.get(
            'hot_flow_chlorine_dioxide', None)
        if hot_flow_chlorine_dioxide:
            self._validateReportValue(
                setting=rangesettings.chlorine_dioxide,
                value=hot_flow_chlorine_dioxide,
                value_name='hot_flow_chlorine_dioxide',
            )

        # VALORI DI TEMPERATURA
        cold_temperature = input.get('cold_temperature', None)
        if cold_temperature:
            self._validateReportValue(
                setting=rangesettings.cold_temperature,
                value=cold_temperature,
                value_name='cold_temperature',
            )
        cold_flow_temperature = input.get('cold_flow_temperature', None)
        if cold_flow_temperature:
            self._validateReportValue(
                setting=rangesettings.cold_flow_temperature,
                value=cold_flow_temperature,
                value_name='cold_flow_temperature',
            )
        hot_temperature = input.get('hot_temperature', None)
        if hot_temperature:
            self._validateReportValue(
                setting=rangesettings.hot_temperature,
                value=hot_temperature,
                value_name='hot_temperature',
            )
        hot_flow_temperature = input.get('hot_flow_temperature', None)
        if hot_flow_temperature:
            self._validateReportValue(
                setting=rangesettings.hot_flow_temperature,
                value=hot_flow_temperature,
                value_name='hot_flow_temperature',
            )

        report = report_model(
            sample_range=fields_with_ids.get('sample_range'),
            wsp=fields_with_ids.get('wsp'),
            risk_level=fields_with_ids.get('wsp').risk_level,
            rangesettings=rangesettings,
            sampling_date=sampling_date,
            review_date=review_date,

            cold_ufcl=cold_ufcl,
            cold_flow_ufcl=cold_flow_ufcl,
            hot_ufcl=hot_ufcl,
            hot_flow_ufcl=hot_flow_ufcl,

            cold_temperature=cold_temperature,
            cold_flow_temperature=cold_flow_temperature,
            hot_temperature=hot_temperature,
            hot_flow_temperature=hot_flow_temperature,

            cold_chlorine_dioxide=cold_chlorine_dioxide,
            cold_flow_chlorine_dioxide=cold_flow_chlorine_dioxide,
            hot_chlorine_dioxide=hot_chlorine_dioxide,
            hot_flow_chlorine_dioxide=hot_flow_chlorine_dioxide,

            cold_ufcl_type=fields_with_ids.get('cold_ufcl_type'),
            cold_flow_ufcl_type=fields_with_ids.get('cold_flow_ufcl_type'),
            hot_ufcl_type=fields_with_ids.get('hot_ufcl_type'),
            hot_flow_ufcl_type=fields_with_ids.get('hot_flow_ufcl_type'),

            cold_ufcl_sampling_selection=fields_with_ids.get(
                'cold_ufcl_sampling_selection'),
            cold_flow_ufcl_sampling_selection=fields_with_ids.get(
                'cold_flow_ufcl_sampling_selection'),
            hot_ufcl_sampling_selection=fields_with_ids.get(
                'hot_ufcl_sampling_selection'),
            hot_flow_ufcl_sampling_selection=fields_with_ids.get(
                'hot_flow_ufcl_sampling_selection'),

            notes_actions=notes_actions,
            after_sampling_status=after_sampling_status,
        )

        report.save()
        return report
