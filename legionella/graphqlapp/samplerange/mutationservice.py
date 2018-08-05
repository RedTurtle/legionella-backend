# -*- coding: utf-8 -*-
from graphqlapp.utils import extract_value_from_input
from .models import SampleRange as samplerange_model
from graphql import GraphQLError
from django.core.exceptions import ObjectDoesNotExist
from ..settings.service import SettingService
from .service import check_samplerange_block
from ..samplerange_freeze.service import SampleRangeFreezeService
from datetime import datetime


class SampleRangeMutationService(object):

    def deleteSampleRange(self, input):
        try:
            samranobj = extract_value_from_input(
                input,
                'samplerange_id',
                'SampleRange',
                samplerange_model)
        except ObjectDoesNotExist as err:
            raise GraphQLError(
                u'Problemi durante il recupero di un '
                + u'intervallo di campionamento.'
            )

        if samranobj.manager_block or \
            samranobj.tecnico_block or \
                samranobj.final_block:
            raise GraphQLError(
                u'Non puoi cancellare un intervallo di campionamento '
                + u'che è stato bloccato o parzialmente bloccato.'
            )

        return samranobj.delete()

    def updateSampleRange(self, input, user_groups):
        settingService = SettingService()

        try:
            samranobj = extract_value_from_input(
                input,
                'samplerange_id',
                'SampleRange',
                samplerange_model)
        except ObjectDoesNotExist:
            raise GraphQLError(
                u'Problemi durante il recupero di un '
                + u'intervallo di campionamento.'
            )

        # Raccolgo le informazioni sui permessi dell'utente
        param = {}
        param['setting_type'] = 'field_permission'
        param['value__contains'] = 'SampleRange.'
        param['owner__in'] = user_groups

        fields_with_permission = settingService.getSettingListByDict(param)

        # PRIMO STEP DI CONTROLLI
        # controllo sui vari block
        # passato questo controllo, si stanno modifcando i dati
        if samranobj.final_block:
            raise GraphQLError(u"Non è possibile modificare un Intervallo di "
                               u"campionamento che è stato finalizzato.")

        if 'manager_block' in input:
            if check_samplerange_block('manager_block',
                                       fields_with_permission):
                samranobj.manager_block = True
                samranobj.save()
                return samranobj

        if 'tecnico_block' in input:
            if check_samplerange_block('tecnico_block',
                                       fields_with_permission):
                samranobj.tecnico_block = True
                samranobj.save()
                return samranobj

        # SECONDO STEP DI CONTROLLI - sui singoli campi modificabili
        # controllo se è stato messo un blocco parziale, nel caso in cui sia
        # stato messo allora non deve essere possibile modificare i campi
        # relativi a quel block.
        # recupero i campi manager_block e tecnico_block

        if samranobj.manager_block:
            # controllo che all'interno dell'input ci siano campi bloccati
            for field in fields_with_permission:
                # TODO -> da fixare questo controllo
                if (field.value.split('SampleRange.', 1)[1] in input and
                        field.value.split('SampleRange.', 1)[1] != u'final_block'):
                    raise GraphQLError(
                        u'Non è possibile modificare il campo {0}'.format(
                            field.value) +
                        u', perchè il blocco manager è già stato attivato.')
        elif samranobj.tecnico_block:
            # controllo che all'interno dell'input ci siano campi bloccati
            for field in fields_with_permission:
                if field.value.split('SampleRange.', 1)[1] in input:
                    raise GraphQLError(
                        u'Non è possibile modificare il campo {0}'.format(
                            field.value) +
                        u', perchè il blocco tecnico è già stato attivato.')

        if input.get('samplerange_id', None):
            # aggiorno i campi che non blocchi
            if 'dates_list' in input.keys():
                samranobj.dates_list = input.get('dates_list', None)
            if 'company' in input.keys():
                samranobj.company = input.get('company', None)
            if 'title' in input.keys():
                samranobj.title = input.get('title', None)
            if 'description' in input.keys():
                samranobj.description = input.get('description', None)
            if 'filter_on' in input.keys():
                samranobj.filter_on = input.get('filter_on', None)

            # controllo sui blocchi
            manager_block = input.get('manager_block', None)
            tecnico_block = input.get('tecnico_block', None)
            final_block = input.get('final_block', None)

            # sistemare i controlli qui
            if manager_block:
                samranobj.manager_block = True
            elif tecnico_block:
                samranobj.tecnico_block = True
            if final_block:
                if samranobj.manager_block and samranobj.tecnico_block:
                    samranobj.final_block = True

                    # Chiamo il service per il freeze del sample range
                    sampleRangeFreezeService = SampleRangeFreezeService()
                    freeze_date, reportFreezeList = sampleRangeFreezeService.freeze(
                        samranobj)
                    if freeze_date:
                        samranobj.freeze_date = freeze_date
                        samranobj.reports_freeze = reportFreezeList
                    else:
                        raise GraphQLError(
                            u"Qualcosa è andato storto con il blocco" +
                            u"dell'intervallo di campionamento.")

                else:
                    raise GraphQLError(
                        u"Non si può bloccare l'intervallo di campionamento," +
                        u"senza il blocco tecnico e manager.")

            samranobj.save()
            return samranobj

    def createSampleRange(self, input):
        dates = input.get('dates_list')
        ordered = [datetime.strptime(el, "%Y-%m-%d").date() for el in dates]

        # GraphQL non si sta comportando a dovere con le stringhe vuote quindi
        # in questo caso facciamo il controllo a mano per i dati obbligatori.
        if not dates or not input.get('company') or not input.get('title'):
            return GraphQLError(
                u"Le date, l'azienda ed il titolo sono campi obbligatori. "
                u"Per favore: compila i campi mancanti."
            )

        samplerange = samplerange_model(
            dates_list=sorted(ordered),
            company=input.get('company'),
            title=input.get('title'),
            description=input.get('description'),
            filter_on=input.get('filter_on')
        )

        samplerange.save()
        return samplerange
