# -*- coding: utf-8 -*-
from ..graphQL_genericSchema.schema import AlertLevel
from ..report.service import ReportService
from ..samplerange.models import SampleRange as samplerange_model
from ..wsp.service import WspService
from .models import Structure as structure_model


class StructureService(object):

    def getStructureByType(self, struct_type=None):
        if not struct_type:
            return structure_model.objects.all()
        else:
            return structure_model.objects.filter(
                struct_type__value=struct_type
            )

    def _ufclLevelCalculation(self, value, setting):
        for ran in setting:
            if 'from' in ran.keys() and 'to' in ran.keys():
                if value >= ran['from'] and value <= ran['to']:
                    return ran
            elif 'from' in ran.keys() and 'to' not in ran.keys():
                if value >= ran['from']:
                    return ran
            else:
                if value <= ran['to']:
                    return ran

    def aggregatedSamplesCold(self, structure):
        # numero di campionamenti previsti per acqua fredda per struttura
        wspService = WspService()
        param = {'structure': structure}
        wspList = wspService.getWspListByDict(param)

        samples = 0
        if wspList:
            for wsp in wspList:
                if wsp.cold:
                    samples += 1
                if wsp.cold_flow:
                    samples += 1

        return samples

    def aggregatedSamplesHot(self, structure):
        # numero di campionamenti previsti per acqua calda per struttura
        wspService = WspService()
        param = {'structure': structure}
        wspList = wspService.getWspListByDict(param)

        samples = 0
        if wspList:
            for wsp in wspList:
                if wsp.hot:
                    samples += 1
                if wsp.hot_flow:
                    samples += 1

        return samples

    def _newestSampleRange(self, wspList):
        # data una lista di wsp mi trova il samplerange
        # piu recente senza filtro
        reportService = ReportService()
        param = {}
        newestSR = {}

        if wspList:
            for wsp in wspList:
                param['wsp'] = wsp
                reportList = reportService.getReportListByDict(param)
                if reportList:
                    for report in reportList:
                        s = report.sample_range
                        rdl = sorted(s.dates_list, reverse=True)
                        if not s.filter_on:
                            if 'start_date' in newestSR.keys():
                                if rdl[0] > newestSR['start_date']:
                                    newestSR['start_date'] = rdl[0]
                                    newestSR['id_sample_range'] = s.id
                            else:
                                newestSR['start_date'] = rdl[0]
                                newestSR['id_sample_range'] = s.id

        return newestSR

    def _worstLevel(self, al, values, ranges, structure):
        result = None
        for val in values.keys():
            if values[val]:
                ran = self._ufclLevelCalculation(
                    value=values[val],
                    setting=ranges
                )
                if ran:
                    if result:
                        if result['priority'] > ran['priority']:
                            result = ran
                    else:
                        result = ran
        if result:
            return result['level']

    def alertLevel(self, structure):
        # calcola le percentuali di livelli di allerta per ogni struttura
        # prendendo il piu recente samplerange con filtro non attivo
        wspService = WspService()
        reportService = ReportService()

        param = {'structure': structure}
        al = AlertLevel()

        wspList = wspService.getWspListByDict(param)

        # count_cold = 0
        # count_hot = 0
        count_report = 0

        # cerco il sampleRange piu recente della structure in esame
        # e che non sia con filtro
        newestSR = self._newestSampleRange(wspList=wspList)

        if newestSR:

            newestSR = samplerange_model.objects.get(
                id=newestSR['id_sample_range'])

            reportList = []
            if newestSR.final_block:
                for report_dict in newestSR.reports_freeze:
                    reportList.append(report_dict)
            else:
                # tutti i report che hanno l'id dei un wsp e l'id del mio sr
                param = {
                    'sample_range__id': newestSR.id,
                    'wsp__in': [wsp for wsp in wspList]
                }
                reportList = reportService.getReportListByDict(param)

            # mi calcolo le percentuali di legionella per ogni alertLevel
            # sia per acqua calda che per per acqua fredda
            if reportList:
                for report in reportList:

                    count_report += 1

                    cold_ufcl = None
                    cold_flow_ufcl = None
                    hot_ufcl = None
                    hot_flow_ufcl = None
                    if newestSR.final_block:
                        ranges = report['rangesettings']['ufcl']

                        if 'cold_ufcl' in report.keys():
                            cold_ufcl = report['cold_ufcl']
                        if 'cold_flow_ufcl' in report.keys():
                            cold_flow_ufcl = report['cold_flow_ufcl']
                        if 'hot_ufcl' in report.keys():
                            hot_ufcl = report['hot_ufcl']
                        if 'hot_flow_ufcl' in report.keys():
                            hot_flow_ufcl = report['hot_flow_ufcl']
                    else:
                        ranges = report.rangesettings.ufcl

                        cold_ufcl = report.cold_ufcl
                        cold_flow_ufcl = report.cold_flow_ufcl
                        hot_ufcl = report.hot_ufcl
                        hot_flow_ufcl = report.hot_flow_ufcl

                    values = {
                        'cold_ufcl': cold_ufcl,
                        'cold_flow_ufcl': cold_flow_ufcl
                    }
                    level = self._worstLevel(
                        al=al.alCold,
                        values=values,
                        ranges=ranges,
                        structure=structure
                    )
                    if level:
                        setattr(al.alCold, level, getattr(
                            al.alCold, level) + 1)

                    values = {
                        'hot_ufcl': hot_ufcl,
                        'hot_flow_ufcl': hot_flow_ufcl
                    }
                    level = self._worstLevel(
                        al=al.alHot,
                        values=values,
                        ranges=ranges,
                        structure=structure
                    )
                    if level:
                        setattr(al.alHot, level, getattr(al.alHot, level) + 1)

                # calcolo delle percentuali
                for attr in vars(al.alCold).keys():
                    if getattr(al.alCold, attr) > 0:
                        temp = (100 * getattr(al.alCold, attr)) / count_report
                        setattr(al.alCold, attr, temp)

                for attr in vars(al.alHot).keys():
                    if getattr(al.alHot, attr) > 0:
                        temp = (100 * getattr(al.alHot, attr)) / count_report
                        setattr(al.alHot, attr, temp)

        return al
