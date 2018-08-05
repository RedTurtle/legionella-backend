# -*- coding: utf-8 -*-
from ..samplerange.models import SampleRange as samplerange_model
from ..settings.service import SettingService
from .models import Document as document_model
from django.core.exceptions import ObjectDoesNotExist
from graphql import GraphQLError
from graphqlapp.utils import extract_value_from_input, humanbytes

import os


class DocumentMutationService(object):

    def deleteDocument(self, input):
        """
        cancellazione di un file
        input:
            input: dict
        output:
            ritorna una tupla composta da:
                int: numero di oggetti eliminati
                dict: che indica il numero di cancellazioni per quel tipo
                      di oggetto
            esempio:
                (1, {'document.Entry': 1})
        """
        try:
            documentobj = extract_value_from_input(
                input=input,
                field_id='document_id',
                model_type='Document',
                model=document_model
            )
        except ObjectDoesNotExist:
            raise GraphQLError(
                u'Ci sono stati problemi durante il recupero del documento.'
            )

        try:
            # Qui c'è l'effettiva eliminazione del file dal DISCO (non dal DB).
            documentobj.document.delete()
        except Exception:
            raise GraphQLError(
                u'Problemi durante la cancellazione del documento.'
            )

        return documentobj.delete()

    def uploadFile(self, data, input):
        """
        upload di un nuovo file
        input:
            data: i file passati nella request
            input: dict
        output:
            -
        """
        settingService = SettingService()

        try:
            samranobj = extract_value_from_input(
                input,
                'samplerange_id',
                'SampleRange',
                samplerange_model)
        except ObjectDoesNotExist:
            raise GraphQLError(
                u'Problemi durante il recupero ' +
                u'dell\'intervallo di campionamento.'
            )

        doc = document_model(
            document=data,
            description=input.get('file_description', ''),
            samplerange=samranobj)

        # recupero il setting della grandezza massima del file consentita
        settingList = settingService.getSettingBySettingType(
            setting_type='max_upload_size'
        )
        sizelimit = settingList[0] if settingList else None

        # Facciamo qui i controlli del caso
        if doc.document.size > sizelimit.int_value:
            raise GraphQLError(u"File troppo grande. Dimensione massima "
                               u"consentita: {}. "
                               u"Il file invece è {}".format(
                                   humanbytes(sizelimit.int_value),
                                   humanbytes(doc.document.size)))

        filename, file_extension = os.path.splitext(doc.document.name)
        allowedext = settingService.getSettingBySettingType(
            setting_type='allowed_file_ext'
        )

        if file_extension not in [ext.value for ext in allowedext]:
            raise GraphQLError(
                u"Estensione file non ammessa: {}".format(file_extension))

        doc.save()
