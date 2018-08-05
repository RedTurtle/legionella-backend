# -*- coding: utf-8 -*-
from ..graphQL_genericSchema.schema import GenericAlertLevel
from ..report.service import ReportService
from ..samplerange.service import SampleRangeService
from ..structure.models import Structure as structure_models
from ..structure.service import StructureService
from ..wsp.service import WspService
from .service import ChartSchemaService
from graphqlapp.utils import extract_value_from_input

import graphene


class ChartRanges(graphene.ObjectType):

    class Meta:
        interfaces = (GenericAlertLevel, )

    def __init__(self):
        self.perfect = 0
        self.good = 0
        self.bad = 0
        self.danger = 0
        self.critical = 0


class Chart(graphene.ObjectType):

    ranges = graphene.Field(ChartRanges)
    totalCount = graphene.Int()
    wspsPercentage = graphene.Int()

    def __init__(self, structList, sampleRangeList, chart_type, struct_type):
        self.totalCount = 0
        self.wspsPercentage = 0

        self.struct_type = struct_type
        self.structList = structList
        self.sampleRangeList = sampleRangeList
        self.chart_type = chart_type

        # funzione che passata una lista di strutture, una lista di
        # samplerange e una lista di tipi di prelievi
        # mi ritorna la lista di report rimanente
        reportService = ReportService()
        self.recentReportList = reportService.getRecentReportList(
            sampleRangeList=self.sampleRangeList,
            structList=self.structList,
            type_list=self.chart_type.keys()
        )

    def resolve_ranges(self, info, **input):
        # il numero di campionameni divisi per livello di allerta
        chartSchemaService = ChartSchemaService()
        return chartSchemaService.chartRangesLevel(
            chart_type=self.chart_type,
            recentReportList=self.recentReportList,
            ranges=ChartRanges()
        )

    def resolve_totalCount(self, info, **input):
        # numero totale di report, che hanno campionamnti per un certo
        # tipo di acqua, presi da una lista di samplerange e relativi
        # a wsp che fanno parte di strutture presenti in un'altra lista
        chartSchemaService = ChartSchemaService()
        ranges = chartSchemaService.chartRangesLevel(
            chart_type=self.chart_type,
            recentReportList=self.recentReportList,
            ranges=ChartRanges()
        )
        tot = 0
        for key in vars(ranges):
            tot += getattr(ranges, key)
        return tot

    def resolve_wspsPercentage(self, info, **input):
        # percentuale dei wsp presi in esame in un certo intervallo di tempo
        # TODO - filtrare anche per tipologia di struttura
        wspService = WspService()
        totalWsp = None
        if self.struct_type:
            totalWsp = wspService.getAllWspBySampleTypeAndStructType(
                type_list=self.chart_type.keys(),
                struct_type=self.struct_type,
            )
        else:
            totalWsp = wspService.getAllWspBySampleType(
                type_list=self.chart_type.keys(),
            )

        # filtrare i report per i prelievi effettivamente fatti
        # controllare che almeno uno dei prelievi previsti sia effettivamente
        # fatto, se non è così, riuovere il report dal conteggio
        report_count = 0
        for report in self.recentReportList:
            flag = False
            for k, v in self.chart_type.items():
                if getattr(report, v) is not None:
                    flag = True
                    break
            if flag:
                report_count += 1

        if len(totalWsp) == 0:
            return 0
        return (100 * report_count) / len(totalWsp)


class ChartContainer(graphene.ObjectType):

    coldChart = graphene.Field(Chart)
    hotChart = graphene.Field(Chart)

    def __init__(self, struct_type, startDate, endDate, struct_id):
        # recupero la lista di strutture di un certo tipo
        self.struct_type = struct_type
        self.structList = []
        structureService = StructureService()

        # La precedenza viene data a struct_id: se lui è specificato, allora
        # restituisco il singolo elemento con quell'id.
        if struct_type and not struct_id:
            self.structList = structureService.getStructureByType(
                struct_type=struct_type
            )
        elif struct_id:
            self.structList.append(
                extract_value_from_input(
                    input={'struct_id': struct_id},
                    field_id='struct_id',
                    model_type='Structure',
                    model=structure_models,
                )
            )
        else:
            self.structList = structureService.getStructureByType()

        # recupero i samplerange in un certo intervallo
        self.sampleRangeList = []
        if startDate and endDate:
            sampleRangeService = SampleRangeService()
            self.sampleRangeList = sampleRangeService.getSampleRangeByStartDateAndEndDateAndFilter(
                startDate=startDate,
                endDate=endDate,
                filter_on=False
            )

    def resolve_coldChart(self, info, **input):
        return Chart(
            structList=self.structList,
            struct_type=self.struct_type,
            sampleRangeList=self.sampleRangeList,
            chart_type={'cold': 'cold_ufcl', 'cold_flow': 'cold_flow_ufcl'}
        )

    def resolve_hotChart(self, info, **input):
        return Chart(
            structList=self.structList,
            struct_type=self.struct_type,
            sampleRangeList=self.sampleRangeList,
            chart_type={'hot': 'hot_ufcl', 'hot_flow': 'hot_flow_ufcl'}
        )
