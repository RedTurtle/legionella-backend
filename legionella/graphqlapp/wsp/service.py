# -*- coding: utf-8 -*-
from ..report.service import ReportService
from .models import Wsp as wsp_model
from graphqlapp.utils import extract_value_from_input


class WspService(object):

    def getWspById(self, input):
        wsp = extract_value_from_input(
            input=input,
            field_id='id',
            model_type='Wsp',
            model=wsp_model
        )

        return wsp

    def getWspListByDict(self, param=None):
        return wsp_model.objects.filter(
            **param
        )

    def getAllWspBySampleType(self, type_list):
        kwargs = {}
        for t in type_list:
            kwargs[t] = True
        return wsp_model.objects.dynamic_or(
            **kwargs
        )

    def getAllWspBySampleTypeAndStructType(self, type_list, struct_type):
        kwargs = {}
        for t in type_list:
            kwargs[t] = True
        return wsp_model.objects.dynamic_or(
            **kwargs
        ).filter(structure__struct_type__value=struct_type)

    def NextReviewDate(self, wsp):
        # tutti i report di un wsp ordinati per sampling_date
        reportService = ReportService()

        param = {'wsp': wsp}
        reportList = reportService.getReportListByDict(param, '-sampling_date')

        review_date = None
        if reportList:
            if reportList[0].review_date:
                review_date = str(
                    reportList[0].review_date.month
                ) + "/" + str(reportList[0].review_date.year)
            else:
                review_date = "-"

        return review_date

    def AlertLevel(self, wsp):
        # valore peggiore di legionella dell'ultimo rap fatto su questo wsp
        reportService = ReportService()
        values = ['cold_ufcl', 'cold_flow_ufcl', 'hot_ufcl', 'hot_flow_ufcl']

        # tutti i report di un wsp ordinati per sampling_date
        param = {'wsp': wsp}
        reportList = reportService.getReportListByDict(param, '-sampling_date')

        if reportList:

            worst_level = 4
            worst_label = ""

            range_ufcl = reportList[0].rangesettings.ufcl

            for val in values:
                if range_ufcl:
                    for ran in range_ufcl:
                        if 'priority' in ran.keys():
                            if 'from' in ran.keys() and 'to' in ran.keys():
                                if getattr(reportList[0], val) >= ran['from']:
                                    if getattr(
                                            reportList[0], val) <= ran['to']:
                                        if ran['priority'] < worst_level:
                                            worst_level = ran['priority']
                                            worst_label = ran['level']
                            elif (
                                'from' in ran.keys() and
                                'to' not in ran.keys()
                            ):
                                if getattr(reportList[0], val) >= ran['from']:
                                    if ran['priority'] < worst_level:
                                        worst_level = ran['priority']
                                        worst_label = ran['level']
                            else:
                                if getattr(reportList[0], val) <= ran['to']:
                                    if ran['priority'] < worst_level:
                                        worst_level = ran['priority']
                                        worst_label = ran['level']
        else:
            worst_label = 'not assigned'

        return worst_label

    def Actions(self):
        # recupero le stesse azioni che sono prosenti del dettaglio del WSP
        # TODO
        pass
