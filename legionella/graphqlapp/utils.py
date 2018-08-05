# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now as timezone_now
from graphene import Node
from graphqlapp.config import ADMIN_ENABLED_MODELS
from graphqlapp.config import REPORT_FIELDS_TO_EXPORT
from graphqlapp.config import SAMPLERANGE_FIELDS_TO_EXPORT
from graphqlapp.config import WSP_FIELDS_TO_EXPORT
from graphqlapp.config import WSP_RISK_LEVEL_FIELDS
from graphqlapp.exportexcel.exportexcel import value_cell_string
from graphqlapp.exportexcel.exportexcel import field2human
from graphqlapp.humanize import TRANSLATIONS


import os
import StringIO
import xlsxwriter


def extract_value_from_input(input, field_id, model_type, model):
    """
    BBB: metodo utilizzato ampiamente nelle mutation per controllare gli ID che
    vengono ricevuti dal front-end.
    """
    settingID = input.get(field_id, None)

    if not settingID:
        return None
    try:
        settingID = int(settingID)
    except ValueError:
        try:
            _type, settingID = Node.from_global_id(settingID)
            assert _type == model_type, \
                u"Expected a {0} object, found {1}".format(model_type, _type)
        except Exception:
            raise Exception(
                u"Received wrong id for querying the db. "
                u"{0}: {1}".format(field_id, settingID))
    try:
        return model.objects.get(id=settingID)
    except ObjectDoesNotExist:
        raise Exception(
            u"Non esiste nessun Wsp con questo id nel database. "
            u"{0}: {1}".format(field_id, settingID))


def upload_to(instance, filename):
    """ Metodo per la generazione del percorso di salvataggio di un allegato
    nel file system.
    """
    now = timezone_now()
    filename_base, filename_ext = os.path.splitext(filename)
    base_folder = u"attachments/"
    return u"{}{}{}{}".format(
        base_folder,
        now.strftime("%Y/%m/"),
        filename_base,
        filename_ext.lower()
    )


def humanbytes(B):
    """
    Restituisce i byte ricevuti in ingresso come una stringa
    human friendly (con anche l'unità di misura: KB, MB, GB, or TB).
    :)
    """
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2)  # 1,048,576
    GB = float(KB ** 3)  # 1,073,741,824
    TB = float(KB ** 4)  # 1,099,511,627,776

    # NOTA: ci sono sia dei print che dei return. Questo perchè, quando lo
    # uso come script, il return non viene stampato a terminale.
    # Non so se ci sia un metodo migliore per evitare questo comportamento.
    if B < KB:
        print '{0} {1}'.format(B, 'Bytes' if 0 == B > 1 else 'Byte')
        return '{0} {1}'.format(B, 'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
        print '{0:.2f} KB'.format(B/KB)
        return '{0:.2f} KB'.format(B/KB)
    elif MB <= B < GB:
        print '{0:.2f} MB'.format(B/MB)
        return '{0:.2f} MB'.format(B/MB)
    elif GB <= B < TB:
        print '{0:.2f} GB'.format(B/GB)
        return '{0:.2f} GB'.format(B/GB)
    elif TB <= B:
        print '{0:.2f} TB'.format(B/TB)
        return '{0:.2f} TB'.format(B/TB)


def get_model_admin_perms(request, model_name):
    """ Questo metodo viene utilizzato nei ModelAdmin personalizzati per
    decidere se mostarli o meno nell'Admin Site.

    I permessi di "visibilità" sono in base al gruppo.
    La lista dei modelli abilitati relativi ai gruppi è nel config file,
    dentro a ADMIN_ENABLED_MODELS.
    """
    if request.user.is_superuser:
        return True

    groups = request.user.groups.all()
    for group in groups:
        models_list = ADMIN_ENABLED_MODELS.get(group.name)
        if models_list:
            if model_name in models_list:
                # In questo caso lo può vedere
                return True
            else:
                return False


def create_excel_file(sampleranges):
    """ Creiamo il file excel
    """

    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    # worksheet.write('A1', 'Test output file excel')

    columns_names = []
    row = 1
    col = 0

    for samplerange in sampleranges:
        for report in samplerange.reports_freeze:
            col = 0
            # campi dei WSP
            for wsp_field in WSP_FIELDS_TO_EXPORT:
                if row == 1:
                    columns_names.append(field2human('wsp', wsp_field))
                try:
                    value = report['wsp'][wsp_field]

                    if wsp_field == 'operative_status':
                        value = value_cell_string(
                            'wsp',
                            wsp_field,
                            value
                        )

                except KeyError:
                    value = 'n.p.'

                worksheet.write(row, col, value)
                col += 1

            # campi dei SAMPLE_RANGE
            for sr_field in SAMPLERANGE_FIELDS_TO_EXPORT:
                if row == 1:
                    columns_names.append(field2human('samplerange', sr_field))
                value = getattr(samplerange, sr_field)
                cell_string = value_cell_string(
                    'samplerange',
                    sr_field,
                    value
                )
                worksheet.write(row, col, cell_string)
                col += 1

            # campi del REPORT
            for rep_field in REPORT_FIELDS_TO_EXPORT:
                if row == 1:
                    columns_names.append(field2human('report', rep_field))
                try:
                    value = report[rep_field]

                    value = value_cell_string(
                        'report',
                        rep_field,
                        value
                    )

                except KeyError:
                    value = 'n.p.'

                worksheet.write(row, col, value)
                col += 1

            row += 1

    col = 0
    for name in columns_names:
        worksheet.write(0, col, name)
        col += 1

    workbook.close()

    # mettiamo il file excel in una variabile
    xlsx_data = output.getvalue()

    return xlsx_data


def humanize_string(text):
    """ Funzione per la 'traduzione' di stringhe di sviluppo in testi più
    chiari e funzionali per il cliente.
    Rende più 'umane' le stringhe che gli vengono passate.
    """

    return TRANSLATIONS.get(text, text)
