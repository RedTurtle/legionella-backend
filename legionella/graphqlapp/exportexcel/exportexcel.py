# -*- coding: utf-8 -*-

from graphqlapp.config import WSP_FIELD_HUMAN_READABLE
from graphqlapp.config import SAMPLERANGE_FIELD_HUMAN_READABLE
from graphqlapp.config import REPORT_FIELD_HUMAN_READABLE


def value_cell_string(modelname, fieldname, value):
    """ Ci sono dati da inserire nelle celle che non sono disponibili al
    primo livello del dizionario di un report congelato.

    Questa funzione ci aiuta a costruire la stringa da scrivere dentro ad
    un'unica cella senza sporcare troppo la funzione principale di esportazione

    modelname = il nome del modello a cui fieldname è riferito
    fieldname = il nome del field/attributo del modello
    value = l'effettito contenuto di fieldname nel dizionario
    """

    if modelname == 'samplerange':
        if fieldname == 'dates_list':
            stringa = []
            for elem in value:
                stringa.append(elem.strftime("%Y-%m-%d"))
            return ', '.join(stringa)

        if fieldname == 'company' or \
           fieldname == 'description' or \
           fieldname == 'title':
            return value

        if fieldname == 'filter_on':
            return value

        if fieldname == 'freeze_date':
            return value.strftime("%Y-%m-%d")

    elif modelname == 'report':
        if fieldname == 'coldFlowUfclType' or \
            fieldname == 'coldUfclType' or \
            fieldname == 'hotFlowUfclType' or \
            fieldname == 'hotUfclType':
            return value['value']  # tipo di legionella
        elif fieldname == 'coldFlowUfclSamplingSelection' or \
            fieldname == 'coldUfclSamplingSelection' or \
            fieldname == 'hotFlowUfclSamplingSelection' or \
            fieldname == 'hotUfclSamplingSelection':
            return value['value']  # selezione radio button (es: > 100)
        elif fieldname == 'coldFlowUfcl' or \
            fieldname == 'coldUfcl' or \
            fieldname == 'hotFlowUfcl' or \
            fieldname == 'hotUfcl' or \
            fieldname == 'coldFlowTemperature' or \
            fieldname == 'coldTemperature' or \
            fieldname == 'hotFlowTemperature' or \
            fieldname == 'hotTemperature' or \
            fieldname == 'coldFlowChlorineDioxide' or \
            fieldname == 'hotFlowChlorineDioxide' or \
            fieldname == 'hotChlorineDioxide' or \
            fieldname == 'coldChlorineDioxide':
            return value
        elif fieldname == 'coldFlowUfclAlertLevel':
            return value
        elif fieldname == 'samplingDate':
            return value.split(' ')[0]


    elif modelname == 'wsp':
        if fieldname == 'operative_status':
            if value:
                return 'Si'
            else:
                return 'No'



def field2human(modelname, fieldname):
    """ Questa funzione prende in ingresso il nome di un field di un oggetto.
    Se trova una sua traduzione/stringa human readable nel dizionario dentro a
    config.py (FIELD_HUMAN_READABLE), allora restituisce quella stringa,
    altrimenti restituisce il nome originale del campo.

    modelname: specifica per quale modello è la traduzione
    """

    if modelname == 'wsp':
        to_human = WSP_FIELD_HUMAN_READABLE.get(fieldname, None)
    elif modelname == 'samplerange':
        to_human = SAMPLERANGE_FIELD_HUMAN_READABLE.get(fieldname, None)
    elif modelname == 'report':
        to_human = REPORT_FIELD_HUMAN_READABLE.get(fieldname, None)

    if to_human:
        return to_human
    else:
        return fieldname
