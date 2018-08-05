# -*- coding: utf-8 -*-
import graphene
from graphene_django import DjangoObjectType

from .models import SampleRange as samplerange_model
from .service import SampleRangeService

from ..graphQL_genericSchema.schema import AggregatedStructures
from ..report.service import ReportService
from ..wsp.service import WspService


class SampleRange(DjangoObjectType):

    class Meta:
        model = samplerange_model
        interfaces = (graphene.Node, )

    sampleRangeId = graphene.ID()
    structureAggregatedSamples = graphene.List(AggregatedStructures)

    def resolve_sampleRangeId(self, info):
        return self.id

    def resolve_structureAggregatedSamples(self, info, **input):

        reportService = ReportService()
        wspService = WspService()

        # TODO ottimizzazione
        # tutti i report di un sample_range
        param = {}
        param['sample_range'] = self
        reportList = reportService.getReportListByDict(param)

        # tutti i wsp dei report
        wspList = []
        if reportList:
            for report in reportList:
                wspList.append(report.wsp)

        # recupero tutte le structure dei wsp
        structureList = []

        if wspList:
            for wsp in wspList:
                if wsp.structure not in structureList:
                    structureList.append(wsp.structure)

        aggregatedStructuresList = []

        if structureList:
            for structure in structureList:

                # calcolo dei wsp per una struttura
                param = {}
                param['structure'] = structure
                wspList = wspService.getWspListByDict(param)

                struct = AggregatedStructures(
                    sampleRangeService=SampleRangeService(),
                    sample_range=self,
                    wspList=wspList,
                    structure=structure
                )

                aggregatedStructuresList.append(struct)

        return aggregatedStructuresList
