# -*- coding: utf-8 -*-
from ..graphQL_genericSchema.schema import (
    DangerLevel,
    DangerLevelTemps,
    ReportOverlay,
    ReportOverlayTemps
)
from ..report.service import ReportService
from ..config import MEASURE_TYPE
from ..wsp.service import WspService
from .models import SampleRange as samplerange_model


class SampleRangeService(object):

    def getSampleRangeListByDict(self, param=None):
        return samplerange_model.objects.filter(
            **param
        )

    def getSampleRangeByStartDateAndEndDate(self, startDate, endDate):
        par_list = [endDate, startDate]
        return samplerange_model.objects.raw(
            ''' select *
                from graphqlapp_samplerange
                where dates_list[1]<=%s and
                      dates_list[array_length(dates_list, 1)]>=%s
                order by dates_list[1] desc''',
            params=par_list)

    def getSampleRangeByStartDateAndEndDateAndFilter(self, startDate, endDate, filter_on):
        par_list = [endDate, startDate, filter_on]
        return samplerange_model.objects.raw(
            ''' select *
                from graphqlapp_samplerange
                where dates_list[1]<=%s and
                      dates_list[array_length(dates_list, 1)]>=%s and
                      filter_on=%s
                order by dates_list[1] desc''',
            params=par_list)

    def samplesNumHot(self, sample_range, structure, wspList):
        # Quanti campionamenti sono stati effettivamente fatti
        # tra quelli che sono previsti per acqua calda
        samples = 0
        reportService = ReportService()

        if wspList:
            for wsp in wspList:
                param = {}
                param['sample_range'] = sample_range
                param['wsp'] = wsp
                reportList = reportService.getReportListByDict(param)

                if reportList:
                    for report in reportList:
                        wsp = report.wsp
                        if wsp.hot:
                            if report.hot_ufcl:
                                samples += 1
                        if wsp.hot_flow:
                            if report.hot_flow_ufcl:
                                samples += 1
        return samples

    def samplesNumCold(self, sample_range, structure, wspList):
        # Quanti campionamenti sono stati effettivamente fatti
        # tra quelli che sono previsti per acqua calda
        samples = 0
        reportService = ReportService()

        if wspList:
            for wsp in wspList:
                param = {}
                param['sample_range'] = sample_range
                param['wsp'] = wsp
                reportList = reportService.getReportListByDict(param)

                if reportList:
                    for report in reportList:
                        wsp = report.wsp
                        if wsp.cold:
                            if report.cold_ufcl:
                                samples += 1
                        if wsp.cold_flow:
                            if report.cold_flow_ufcl:
                                samples += 1
        return samples

    def wspsNum(self, sample_range, wspList):
        # i punti di campionamento per una structure in un sample_range
        # conto i report perche do per scontato che se ce un rapporto
        # allora è associato ad un solo WSP
        reportService = ReportService()
        param = {}
        param['sample_range'] = sample_range

        # tutti i wsp della structure
        reportNum = 0
        if wspList:
            for wsp in wspList:
                param['wsp'] = wsp
                reportNum += len(
                    reportService.getReportListByDict(param)
                )

        return reportNum

    def wspsPercentage(self, sample_range, wspList, structure):
        '''
        Percentuale di wsp di una sottostazione esaminata
        in un certo SampleRange
        '''
        wspService = WspService()

        param = {}
        param['structure'] = structure

        wspsNum = self.wspsNum(sample_range=sample_range, wspList=wspList)
        subWspsList = wspService.getWspListByDict(param)
        subWspsNum = len(subWspsList)
        return (100 * wspsNum) / subWspsNum

    def aggregate(self, sample_range, structure, wspList, values, range_type):
        reportList = []
        reportService = ReportService()

        param = {}
        param['sample_range'] = sample_range

        if wspList:
            for wsp in wspList:
                param['wsp'] = wsp
                reportList.extend(reportService.getReportListByDict(param))

        danger_level = DangerLevel()

        if reportList:
            # prendo il range del primo report
            rangesettings = reportList[0].rangesettings

            worst_value = {}

            totale = len(reportList)

            for report in reportList:

                worst_value['priority'] = 4
                worst_value['value'] = None

                if getattr(report.rangesettings, range_type):
                    for val in values:
                        # controllo che il wsp del report possa fare il prelievo
                        for measure_value in MEASURE_TYPE.values():
                            if val in measure_value:
                                if not getattr(report.wsp, MEASURE_TYPE.keys()[MEASURE_TYPE.values().index(measure_value)]) or \
                                        getattr(report, val) is None:
                                    continue
                                else:
                                    # fra i prelievi fatti su un certo report
                                    # trovo il valore peggiore fra i prelievi
                                    for ran in getattr(report.rangesettings, range_type):
                                        if 'from' in ran.keys() and 'to' in ran.keys():
                                            if getattr(report, val) >= ran['from']:
                                                if getattr(report, val) <= ran['to']:
                                                    if ran['priority'] < worst_value.get('priority'):
                                                        worst_value['priority'] = ran.get(
                                                            'priority')
                                                        worst_value['value'] = ran.get(
                                                            'level')
                                        elif 'from' in ran.keys() and 'to' not in ran.keys():
                                            if getattr(report, val) >= ran['from']:
                                                if ran['priority'] < worst_value.get('priority'):
                                                    worst_value['priority'] = ran.get(
                                                        'priority')
                                                    worst_value['value'] = ran.get(
                                                        'level')
                                        else:
                                            if getattr(report, val) <= ran['to']:
                                                if ran['priority'] < worst_value.get('priority'):
                                                    worst_value['priority'] = ran.get(
                                                        'priority')
                                                    worst_value['value'] = ran.get(
                                                        'level')

                if worst_value['value']:
                    # per ogni report ora so il campionamento peggiore
                    setattr(danger_level, worst_value['value'], getattr(
                        danger_level, worst_value['value']) + 1)
                else:
                    totale -= 1

        if totale != 0:
            for ran in getattr(rangesettings, range_type):
                if getattr(danger_level, ran['level']) > 0:
                    setattr(
                        danger_level,
                        ran['level'],
                        (100 * getattr(danger_level, ran['level'])) / totale
                    )

        return danger_level

    def aggregatedBioxCold(self, sample_range, structure, wspList):
        values = ['cold_chlorine_dioxide', 'cold_flow_chlorine_dioxide']
        range_type = 'chlorine_dioxide'
        return self.aggregate(
            sample_range=sample_range,
            structure=structure,
            wspList=wspList,
            values=values,
            range_type=range_type
        )

    def aggregatedBioxHot(self, sample_range, structure, wspList):
        values = ['hot_chlorine_dioxide', 'hot_flow_chlorine_dioxide']
        range_type = 'chlorine_dioxide'
        return self.aggregate(
            sample_range=sample_range,
            structure=structure,
            wspList=wspList,
            values=values,
            range_type=range_type
        )

    def aggregatedLegionellaHot(self, sample_range, structure, wspList):
        values = ['hot_ufcl', 'hot_flow_ufcl']
        range_type = 'ufcl'
        return self.aggregate(
            sample_range=sample_range,
            structure=structure,
            wspList=wspList,
            values=values,
            range_type=range_type
        )

    def aggregatedLegionellaCold(self, sample_range, structure, wspList):
        values = ['cold_ufcl', 'cold_flow_ufcl']
        range_type = 'ufcl'
        return self.aggregate(
            sample_range=sample_range,
            structure=structure,
            wspList=wspList,
            values=values,
            range_type=range_type
        )

    def aggregatedTemps(self, sample_range, structure, wspList):
        danger_level_temps = DangerLevelTemps()
        values = ['cold_temperature', 'cold_flow_temperature',
                  'hot_temperature', 'hot_flow_temperature']

        for val in values:
            danger_level = self.aggregate(
                sample_range=sample_range,
                structure=structure,
                wspList=wspList,
                values=[val],
                range_type=val
            )
            setattr(danger_level_temps, val, danger_level.copy())
            danger_level.reset()
        return danger_level_temps

    def _rangelevel_toString(self, rangesettings, level):
        range_string_list = []
        elements = [x for x in rangesettings if x['level'] == level]

        for el in elements:
            range_string = ""
            if el.get('from') and not el.get('to'):
                range_string += "> " + str(el['from'])
            elif not el.get('from') and el.get('to'):
                range_string += "< " + str(el['to'])
            elif el.get('from') and el.get('to'):
                range_string += str(el['from']) + " - " + str(el['to'])
            range_string_list.append(range_string)

        # TODO da far tornare la lista intera
        prova = []
        if range_string_list:
            prova.append(range_string_list[0])
        return prova

    def _overlay_calculation(self, values, types, sample_range, structure, wsps_num):
        # è possibile eliminare tutta la parte di worst_value
        report_overlay = ReportOverlay()
        reportService = ReportService()

        param = {}
        param['sample_range'] = sample_range
        param['wsp__structure'] = structure

        # recupero tutti i report
        report_list = reportService.getReportListByDict(param)

        # recupero il range del primo report
        # (dovrebbe essere lo stesso per tutti)
        if report_list:
            # da usare quando vado a tradurre le priority
            rangesettings = report_list[0].rangesettings

            worst_value = {}

            for report in report_list:

                # uso 4 perchè è maggiore di tutte le priorità
                worst_value['priority'] = 4
                worst_value['value'] = ""

                # controllo se il wsp ha prelevamenti di un certo tipo
                for val in values:
                    for measure_value in MEASURE_TYPE.values():
                        if val in measure_value:

                            if not getattr(report.wsp, MEASURE_TYPE.keys()[MEASURE_TYPE.values().index(measure_value)]) or \
                                    getattr(report, val) is None:
                                continue
                            else:
                                for ran in getattr(report.rangesettings, types):
                                    if 'from' in ran.keys() and 'to' in ran.keys():
                                        if getattr(report, val) >= ran['from']:
                                            if getattr(report, val) <= ran['to']:
                                                if ran['priority'] < worst_value.get('priority'):
                                                    worst_value['priority'] = ran.get(
                                                        'priority')
                                                    worst_value['value'] = ran.get(
                                                        'level')
                                    elif ('from' in ran.keys() and
                                          'to' not in ran.keys()):
                                        if getattr(report, val) >= ran['from']:
                                            if ran['priority'] < worst_value.get('priority'):
                                                worst_value['priority'] = ran.get(
                                                    'priority')
                                                worst_value['value'] = ran.get(
                                                    'level')
                                    else:
                                        if getattr(report, val) <= ran['to']:
                                            if ran['priority'] < worst_value.get('priority'):
                                                worst_value['priority'] = ran.get(
                                                    'priority')
                                                worst_value['value'] = ran.get(
                                                    'level')

                if worst_value['value']:
                    getattr(report_overlay, worst_value['value']).wsp_num += 1
                    getattr(report_overlay,
                            worst_value['value']).alert_level = worst_value['value']
                else:
                    wsps_num -= 1

            for key in report_overlay.__dict__.keys():
                getattr(report_overlay, key).range_level = self._rangelevel_toString(
                    getattr(rangesettings, types),
                    key
                )
                if getattr(report_overlay, key).wsp_num != 0:
                    getattr(report_overlay, key).percentage = (
                        100 * getattr(report_overlay, key).wsp_num) / wsps_num

            return report_overlay

    def overlayLegionellaHot(self, sample_range, structure, wspList):
        wsps_num = self.wspsNum(sample_range=sample_range, wspList=wspList)
        values = ['hot_ufcl', 'hot_flow_ufcl']
        report_overlay = self._overlay_calculation(
            values=values,
            types='ufcl',
            sample_range=sample_range,
            structure=structure,
            wsps_num=wsps_num
        )
        return report_overlay

    def overlayLegionellaCold(self, sample_range, structure, wspList):
        wsps_num = self.wspsNum(sample_range=sample_range, wspList=wspList)
        values = ['cold_ufcl', 'cold_flow_ufcl']
        report_overlay = self._overlay_calculation(
            values=values,
            types='ufcl',
            sample_range=sample_range,
            structure=structure,
            wsps_num=wsps_num
        )
        return report_overlay

    def overlayBioxHot(self, sample_range, structure, wspList):
        wsps_num = self.wspsNum(sample_range=sample_range, wspList=wspList)
        values = ['hot_chlorine_dioxide', 'hot_flow_chlorine_dioxide']
        report_overlay = self._overlay_calculation(
            values=values,
            types='chlorine_dioxide',
            sample_range=sample_range,
            structure=structure,
            wsps_num=wsps_num
        )
        return report_overlay

    def overlayBioxCold(self, sample_range, structure, wspList):
        wsps_num = self.wspsNum(sample_range=sample_range, wspList=wspList)
        values = ['cold_chlorine_dioxide', 'cold_flow_chlorine_dioxide']
        report_overlay = self._overlay_calculation(
            values=values,
            types='chlorine_dioxide',
            sample_range=sample_range,
            structure=structure,
            wsps_num=wsps_num
        )
        return report_overlay

    def overlayTemps(self, sample_range, structure, wspList):
        wsps_num = self.wspsNum(sample_range=sample_range, wspList=wspList)
        report_overlay_temps = ReportOverlayTemps()
        values = [
            'cold_temperature',
            'cold_flow_temperature',
            'hot_temperature',
            'hot_flow_temperature'
        ]
        for val in values:
            setattr(report_overlay_temps, val, self._overlay_calculation(
                values=[val],
                types=val,
                sample_range=sample_range,
                structure=structure,
                wsps_num=wsps_num
            ))
        return report_overlay_temps


def check_samplerange_block(block, permissions):
    """ Questa funzione viene usata per controllare se sia possibile modificare
    i block di un intervallo di campionamento.
    return True se va tutto bene.
    """
    for field in permissions:
        if (field.value.split('.')[1] == block):
            return True
    return False
