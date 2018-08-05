# -*- coding: utf-8 -*-
import graphene
from graphene_django import DjangoObjectType

from .models import Report as report_model
from ..graphQL_genericSchema.schema import ReportWorstState
from .service import ReportService


class Report(DjangoObjectType):
    class Meta:
        model = report_model
        interfaces = (graphene.Node, )

    coldUfclAlertLevel = graphene.String()
    coldFlowUfclAlertLevel = graphene.String()
    hotUfclAlertLevel = graphene.String()
    hotFlowUfclAlertLevel = graphene.String()

    coldTemperatureAlertLevel = graphene.String()
    coldFlowTemperatureAlertLevel = graphene.String()
    hotTemperatureAlertLevel = graphene.String()
    hotFlowTemperatureAlertLevel = graphene.String()

    coldChlorineDioxideAlertLevel = graphene.String()
    coldFlowChlorineDioxideAlertLevel = graphene.String()
    hotChlorineDioxideAlertLevel = graphene.String()
    hotFlowChlorineDioxideAlertLevel = graphene.String()

    worstStates = graphene.Field(ReportWorstState)

    # controllo quando tornare i valore di legionella,
    # in modo da tornare i valori di default
    def resolve_cold_ufcl(self, info, **kwargs):
        if self.cold_ufcl_sampling_selection and \
                self.cold_ufcl_sampling_selection.has_legionella_type:
            return self.cold_ufcl
        return 0

    def resolve_cold_flow_ufcl(self, info, **kwargs):
        if self.cold_flow_ufcl_sampling_selection and \
                self.cold_flow_ufcl_sampling_selection.has_legionella_type:
            return self.cold_flow_ufcl
        return 0

    def resolve_hot_ufcl(self, info, **kwargs):
        if self.hot_ufcl_sampling_selection and \
                self.hot_ufcl_sampling_selection.has_legionella_type:
            return self.hot_ufcl
        return 0

    def resolve_hot_flow_ufcl(self, info, **kwargs):
        if self.hot_flow_ufcl_sampling_selection and \
                self.hot_flow_ufcl_sampling_selection.has_legionella_type:
            return self.hot_flow_ufcl
        return 0

    def resolve_worstStates(self, info, **kwargs):
        # SERVICE
        reportService = ReportService()
        worstStates = reportService.worstStates(
            report=self
        )
        return worstStates

    # alert level per legionella
    def resolve_coldUfclAlertLevel(self, info, **kwargs):
        # SERVICE
        reportService = ReportService()
        result = reportService.alertLevel(self, 'cold', 'cold_ufcl', 'ufcl')
        return result.get('level', None) if result else None

    def resolve_coldFlowUfclAlertLevel(self, info, **kwargs):
        # SERVICE
        reportService = ReportService()
        result = reportService.alertLevel(
            self, 'cold_flow', 'cold_flow_ufcl', 'ufcl')
        return result.get('level', None) if result else None

    def resolve_hotUfclAlertLevel(self, info, **kwargs):
        # SERVICE
        reportService = ReportService()
        result = reportService.alertLevel(self, 'hot', 'hot_ufcl', 'ufcl')
        return result.get('level', None) if result else None

    def resolve_hotFlowUfclAlertLevel(self, info, **kwargs):
        # SERVICE
        reportService = ReportService()
        result = reportService.alertLevel(
            self, 'hot_flow', 'hot_flow_ufcl', 'ufcl')
        return result.get('level', None) if result else None

    # alert level per le temperature
    def resolve_coldTemperatureAlertLevel(self, info, **kwargs):
        # SERVICE
        reportService = ReportService()
        result = reportService.alertLevel(
            self,
            'cold',
            'cold_temperature',
            'cold_temperature')
        return result.get('level', None) if result else None

    def resolve_coldFlowTemperatureAlertLevel(self, info, **kwargs):
        # SERVICE
        reportService = ReportService()
        result = reportService.alertLevel(
            self,
            'cold_flow',
            'cold_flow_temperature',
            'cold_flow_temperature')
        return result.get('level', None) if result else None

    def resolve_hotTemperatureAlertLevel(self, info, **kwargs):
        # SERVICE
        reportService = ReportService()
        result = reportService.alertLevel(
            self,
            'hot',
            'hot_temperature',
            'hot_temperature'
        )
        return result.get('level', None) if result else None

    def resolve_hotFlowTemperatureAlertLevel(self, info, **kwargs):
        # SERVICE
        reportService = ReportService()
        result = reportService.alertLevel(
            self,
            'hot_flow',
            'hot_flow_temperature',
            'hot_flow_temperature'
        )
        return result.get('level', None) if result else None

    # alert level per il biossido
    def resolve_coldChlorineDioxideAlertLevel(self, info, **kwargs):
        # SERVICE
        reportService = ReportService()
        result = reportService.alertLevel(
            self,
            'cold',
            'cold_chlorine_dioxide',
            'chlorine_dioxide'
        )
        return result.get('level', None) if result else None

    def resolve_coldFlowChlorineDioxideAlertLevel(self, info, **kwargs):
        # SERVICE
        reportService = ReportService()
        result = reportService.alertLevel(
            self,
            'cold_flow',
            'cold_flow_chlorine_dioxide',
            'chlorine_dioxide'
        )
        return result.get('level', None) if result else None

    def resolve_hotChlorineDioxideAlertLevel(self, info, **kwargs):
        # SERVICE
        reportService = ReportService()
        result = reportService.alertLevel(
            self,
            'hot',
            'hot_chlorine_dioxide',
            'chlorine_dioxide'
        )
        return result.get('level', None) if result else None

    def resolve_hotFlowChlorineDioxideAlertLevel(self, info, **kwargs):
        # SERVICE
        reportService = ReportService()
        result = reportService.alertLevel(
            self,
            'hot_flow',
            'hot_flow_chlorine_dioxide',
            'chlorine_dioxide'
        )
        return result.get('level', None) if result else None
