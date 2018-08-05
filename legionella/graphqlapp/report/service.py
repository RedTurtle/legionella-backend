# -*- coding: utf-8 -*-
from ..graphQL_genericSchema.schema import ReportWorstState
from .models import Report as report_model


class ReportService(object):

    def getReportListByDict(self, param=None, order=None):
        """
        funzione che ritorna una lista di report
        input:
            param: dict con i filtri per i report
            order: string argomenti su cui fare l'ordinamento
        output:
            list di report
        """
        if not order:
            return report_model.objects.filter(
                **param
            )
        else:
            return report_model.objects.filter(
                **param
            ).order_by(order)

    def getRecentReportList(self, sampleRangeList, structList, type_list):
        """
        funzione che ritorna una lista di report
        input:
            sampleRangaList: list di samplerange ordinati dal più recente al
                             più vecchio
            structList: list di strutture
            type_list: list di tipi di prelievi sul wsp
        output:
            list di report
        """
        # sampleRangeList è una lista di sampleRange ordinati dal più recente
        # al più vecchio
        report_list = []
        for sr in sampleRangeList:
            report_list.extend(
                report_model.objects.select_related('wsp').filter(
                    sample_range=sr
                )
            )

        wr_dict = {}
        wsp_list = []
        for r in report_list:
            if r.wsp.id not in wr_dict.keys():
                wr_dict[r.wsp.id] = []
                wr_dict[r.wsp.id].append(r)
                wsp_list.append(r.wsp)
            else:
                wr_dict[r.wsp.id].append(r)

        # devo vedere quali wsp fanno parte delle strutture che voglio
        # prendere in esame
        for wsp in wsp_list:
            if wsp.structure not in structList:
                wr_dict.pop(wsp.id, None)
                continue
            flag = 0
            for t in type_list:
                if getattr(wsp, t):
                    flag = 1
                    break
            if flag == 0:
                wr_dict.pop(wsp.id, None)

        # mi aspetto che il primo elemento di ogni lista di report sia
        # il report più recente di quel wsp
        return [wr_dict[x][0] for x in wr_dict.keys()]

    def alertLevelCalculation(self, value, setting):
        for ran in setting:
            if 'from' in ran.keys() and 'to' in ran.keys():
                if value >= ran['from'] and value <= ran['to']:
                    return {'level': ran['level'], 'priority': ran['priority']}
            elif 'from' in ran.keys() and 'to' not in ran.keys():
                if value >= ran['from']:
                    return {'level': ran['level'], 'priority': ran['priority']}
            else:
                if value <= ran['to']:
                    return {'level': ran['level'], 'priority': ran['priority']}

    def alertLevel(self, report, wspTypeSample, reportTypeSample, typeRange):
        if getattr(report.wsp, wspTypeSample):
            result = self.alertLevelCalculation(
                value=getattr(report, reportTypeSample),
                setting=getattr(report.rangesettings, typeRange)
            )
            if result:
                return result

    def worstValue(self, levelList):
        # trovo il livello peggiore di una lista di livelli di allerta
        worst_level = 4
        worst_label = None

        for level in levelList:
            if level:
                if level.get('priority') < worst_level:
                    worst_level = level['priority']
                    worst_label = level['level']

        return worst_label

    def worstStates(self, report):
        # non lo separo in piu resolver perche sono dati che non verranno
        # mai chiesti separati
        worstStates = ReportWorstState()

        results = []
        cold = []
        cold.append(self.alertLevel(
            report=report,
            wspTypeSample='cold',
            reportTypeSample='cold_ufcl',
            typeRange='ufcl'
        ))
        cold.append(self.alertLevel(
            report=report,
            wspTypeSample='cold',
            reportTypeSample='cold_temperature',
            typeRange='cold_temperature'
        ))
        cold.append(self.alertLevel(
            report=report,
            wspTypeSample='cold',
            reportTypeSample='cold_chlorine_dioxide',
            typeRange='chlorine_dioxide'
        ))
        results.extend(cold)
        worstStates.worstStateCold = self.worstValue(cold)

        cold_flow = []
        cold_flow.append(self.alertLevel(
            report=report,
            wspTypeSample='cold_flow',
            reportTypeSample='cold_flow_ufcl',
            typeRange='ufcl'
        ))
        cold_flow.append(self.alertLevel(
            report=report,
            wspTypeSample='cold_flow',
            reportTypeSample='cold_flow_temperature',
            typeRange='cold_flow_temperature'
        ))
        cold_flow.append(self.alertLevel(
            report=report,
            wspTypeSample='cold_flow',
            reportTypeSample='cold_flow_chlorine_dioxide',
            typeRange='chlorine_dioxide'
        ))
        results.extend(cold_flow)
        worstStates.worstStateColdFlow = self.worstValue(cold_flow)

        hot = []
        hot.append(self.alertLevel(
            report=report,
            wspTypeSample='hot',
            reportTypeSample='hot_ufcl',
            typeRange='ufcl'
        ))
        hot.append(self.alertLevel(
            report=report,
            wspTypeSample='hot',
            reportTypeSample='hot_temperature',
            typeRange='hot_temperature'
        ))
        hot.append(self.alertLevel(
            report=report,
            wspTypeSample='hot',
            reportTypeSample='hot_chlorine_dioxide',
            typeRange='chlorine_dioxide'
        ))
        results.extend(hot)
        worstStates.worstStateHot = self.worstValue(hot)

        hot_flow = []
        hot_flow.append(self.alertLevel(
            report=report,
            wspTypeSample='hot_flow',
            reportTypeSample='hot_flow_ufcl',
            typeRange='ufcl'
        ))
        hot_flow.append(self.alertLevel(
            report=report,
            wspTypeSample='hot',
            reportTypeSample='hot_temperature',
            typeRange='hot_temperature'
        ))
        hot_flow.append(self.alertLevel(
            report=report,
            wspTypeSample='hot_flow',
            reportTypeSample='hot_flow_chlorine_dioxide',
            typeRange='chlorine_dioxide'
        ))
        results.extend(hot_flow)
        worstStates.worstStateHotFlow = self.worstValue(hot_flow)

        worstStates.absoluteWorstState = self.worstValue(results)

        return worstStates
