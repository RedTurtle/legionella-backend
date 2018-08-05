# -*- coding: utf-8 -*-
MEASURE_TYPE = {
    'cold': [
        'cold_ufcl',
        'cold_ufcl_type',
        'cold_ufcl_sampling_selection',
        'cold_temperature',
        'cold_chlorine_dioxide'
    ],
    'cold_flow': [
        'cold_flow_ufcl',
        'cold_flow_ufcl_type',
        'cold_flow_ufcl_sampling_selection',
        'cold_flow_temperature',
        'cold_flow_chlorine_dioxide'
    ],
    'hot': [
        'hot_ufcl',
        'hot_ufcl_type',
        'hot_ufcl_sampling_selection',
        'hot_temperature',
        'hot_chlorine_dioxide'
    ],
    'hot_flow': [
        'hot_flow_ufcl',
        'hot_flow_ufcl_type',
        'hot_flow_ufcl_sampling_selection',
        'hot_flow_temperature',
        'hot_flow_chlorine_dioxide'
    ],
}


ADMIN_ENABLED_MODELS = {
    'manager': [
        'Wsp',
        'Building',
        'Floor',
        'Structure',
        'Sector',
    ],
    'tecnico': [

    ],
}

# -----------------------------------------------
# CONFIGURAZIONE DELL'ESPORTAZIONE DEI FILE EXCEL

REPORT_FIELDS_TO_EXPORT = [
    'samplingDate',
    'coldUfcl',
    'coldUfclSamplingSelection',
    'coldUfclType',
    'coldFlowUfcl',
    'coldFlowUfclSamplingSelection',
    'coldFlowUfclType',
    'hotUfcl',
    'hotUfclSamplingSelection',
    'hotUfclType',
    'hotFlowUfcl',
    'hotFlowUfclSamplingSelection',
    'hotFlowUfclType',
    'hotTemperature',
    'hotFlowTemperature',
    'coldTemperature',
    'coldFlowTemperature',
    'coldChlorineDioxide',
    'coldFlowChlorineDioxide',
    'hotChlorineDioxide',
    'hotFlowChlorineDioxide',
    # 'rangesettings',
    # 'reviewDate',
    # 'worstStates',  # inutili per il report
    # 'coldFlowUfclAlertLevel',
    # 'coldFlowChlorineDioxideAlertLevel',
    # 'hotChlorineDioxideAlertLevel',
    # 'hotTemperatureAlertLevel',
    # 'hotUfclAlertLevel',
    # 'hotFlowTemperatureAlertLevel',
    # 'coldUfclAlertLevel',
    # 'hotFlowChlorineDioxideAlertLevel',
    # 'coldFlowTemperatureAlertLevel',
    # 'hotFlowUfclAlertLevel',
    # 'coldTemperatureAlertLevel',
    # 'coldChlorineDioxideAlertLevel',
]

WSP_FIELDS_TO_EXPORT = [
    'code',
    'description',
    'alert_level',
    'operative_status',
]

SAMPLERANGE_FIELDS_TO_EXPORT = [
    'company',
    'dates_list',
    'description',
    'filter_on',
    'freeze_date',
    'title',
]


WSP_RISK_LEVEL_FIELDS = [
    'description',
    # 'has_legionella_type',
    # 'id',
    'int_value',
    # 'notes_actions_json',
    # 'owner',
    'position',
    'setting_type',
    'value',
]


WSP_FIELD_HUMAN_READABLE = {
    # WSP
    'code': 'codice wsp',
    # 'risk_level': 'livello di rischio wsp',
    'description': 'descrizione wsp',
    'alert_level': 'livello di allerta wsp',
    'operative_status': 'wsp attivo',
}

SAMPLERANGE_FIELD_HUMAN_READABLE = {
    # SAMPLE_RANGE
    'company': 'azienda rilevamenti',
    'dates_list': 'date rilevamenti',
    'filter_on': 'filtri presenti',
    'freeze_date': 'data di conferma rapporto',
    'title': 'nome intervallo di campionamento',
    'description': 'descrizione interv. di campionamento',
}


REPORT_FIELD_HUMAN_READABLE = {
    'samplingDate': 'data campionamento',
    'coldUfcl': 'ufcl - acqua fredda (mg/L)',
    'coldUfclSamplingSelection': 'livello di ufcl selezionato',
    'coldUfclType': 'ceppo legionella acqua fredda',
    'coldFlowUfcl': 'ufcl - acqua fredda scorrimento (mg/L)',
    'coldFlowUfclSamplingSelection': 'livello di ufcl selezionato',
    'coldFlowUfclType': 'ceppo legionella acqua fredda scorrimento',
    'hotUfcl': 'ufcl - acqua calda (mg/L)',
    'hotUfclSamplingSelection': 'livello di ufcl selezionato',
    'hotUfclType': 'ceppo legionella acqua calda',
    'hotFlowUfcl': 'ufcl - acqua calda scorrimento (mg/L)',
    'hotFlowUfclSamplingSelection': 'livello di ufcl selezionato',
    'hotFlowUfclType': 'ceppo legionella acqua calda scorrimento',
    'hotTemperature': u'temperatura acqua calda (°C)',
    'hotFlowTemperature': u'temperatura acqua calda scorrimento (°C)',
    'coldTemperature': u'temperatura acqua fredda (°C)',
    'coldFlowTemperature': u'temperatura acqua fredda scorrimento (°C)',
    'coldChlorineDioxide': 'biossido di cloro - acqua fredda',
    'coldFlowChlorineDioxide': 'biossido di cloro - acqua fredda scorrimento',
    'hotChlorineDioxide': 'biossido di cloro - acqua calda',
    'hotFlowChlorineDioxide': 'biossido di cloro - acqua calda scorrimento',
}
