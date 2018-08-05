# -*- coding: utf-8 -*-
from ..range.freeze import RangeFreeze
from ..wsp.freeze import WspFreeze
from .service import ReportService
from django.forms.models import model_to_dict

import json


class ReportFreeze(object):

    def __init__(self, report):

        # recupero il wsp del report
        self.wsp = WspFreeze(report.wsp).__dict__
        if report.risk_level:
            self.riskLevel = model_to_dict(report.risk_level)
        # recupero il range del report
        self.rangesettings = RangeFreeze(report.rangesettings).__dict__
        # tutti gli altri dati del report
        if report.sampling_date:
            self.samplingDate = report.sampling_date.strftime(
                "%Y-%m-%d %H:%M:%S")

        # TIPI DI LEGIONELLA
        if report.cold_ufcl_type:
            self.coldUfclType = model_to_dict(report.cold_ufcl_type)
        if report.cold_flow_ufcl_type:
            self.coldFlowUfclType = model_to_dict(
                report.cold_flow_ufcl_type
            )
        if report.hot_ufcl_type:
            self.hotUfclType = model_to_dict(report.hot_ufcl_type)
        if report.hot_flow_ufcl_type:
            self.hotFlowUfclType = model_to_dict(
                report.hot_flow_ufcl_type
            )

        # SAMPLING SELECTION
        if report.cold_ufcl_sampling_selection:
            self.coldUfclSamplingSelection = model_to_dict(
                report.cold_ufcl_sampling_selection
            )
        if report.cold_flow_ufcl_sampling_selection:
            self.coldFlowUfclSamplingSelection = model_to_dict(
                report.cold_flow_ufcl_sampling_selection
            )
        if report.hot_ufcl_sampling_selection:
            self.hotUfclSamplingSelection = model_to_dict(
                report.hot_ufcl_sampling_selection
            )
        if report.hot_flow_ufcl_sampling_selection:
            self.hotFlowUfclSamplingSelection = model_to_dict(
                report.hot_flow_ufcl_sampling_selection
            )

        if report.notes_actions:
            if isinstance(report.notes_actions, (dict, list)):
                self.notesActions = report.notes_actions
            else:
                self.notesActions = json.loads(report.notes_actions)
        if report.after_sampling_status:
            self.afterSamplingStatus = report.after_sampling_status
        if report.review_date:
            self.reviewDate = report.review_date.strftime(
                "%Y-%m-%d %H:%M:%S")

        # TEMPERATURE
        if report.cold_temperature:
            self.coldTemperature = report.cold_temperature
        if report.cold_flow_temperature:
            self.coldFlowTemperature = report.cold_flow_temperature
        if report.hot_temperature:
            self.hotTemperature = report.hot_temperature
        if report.hot_flow_temperature:
            self.hotFlowTemperature = report.hot_flow_temperature

        # UFCL
        if report.cold_ufcl:
            self.coldUfcl = report.cold_ufcl
        if report.cold_flow_ufcl:
            self.coldFlowUfcl = report.cold_flow_ufcl
        if report.hot_ufcl:
            self.hotUfcl = report.hot_ufcl
        if report.hot_flow_ufcl:
            self.hotFlowUfcl = report.hot_flow_ufcl

        # CHLORINE DIOXIDE
        if report.cold_chlorine_dioxide:
            self.coldChlorineDioxide = report.cold_chlorine_dioxide
        if report.cold_flow_chlorine_dioxide:
            self.coldFlowChlorineDioxide = report.cold_flow_chlorine_dioxide
        if report.hot_chlorine_dioxide:
            self.hotChlorineDioxide = report.hot_chlorine_dioxide
        if report.hot_flow_chlorine_dioxide:
            self.hotFlowChlorineDioxide = report.hot_flow_chlorine_dioxide

        # AGGREGATI
        reportService = ReportService()
        self.worstStates = reportService.worstStates(report=report).__dict__

        result = reportService.alertLevel(report, 'cold', 'cold_ufcl', 'ufcl')
        self.coldUfclAlertLevel = result.get('level') if result else None
        result = reportService.alertLevel(
            report, 'cold_flow', 'cold_flow_ufcl', 'ufcl')
        self.coldFlowUfclAlertLevel = result.get('level') if result else None
        result = reportService.alertLevel(
            report, 'hot', 'hot_ufcl', 'ufcl')
        self.hotUfclAlertLevel = result.get('level') if result else None
        result = reportService.alertLevel(
            report, 'hot_flow', 'hot_flow_ufcl', 'ufcl')
        self.hotFlowUfclAlertLevel = result.get('level') if result else None

        result = reportService.alertLevel(
            report, 'cold', 'cold_temperature', 'cold_temperature')
        self.coldTemperatureAlertLevel = result.get(
            'level', None) if result else None
        result = reportService.alertLevel(
            report,
            'cold_flow',
            'cold_flow_temperature',
            'cold_flow_temperature')
        self.coldFlowTemperatureAlertLevel = result.get(
            'level', None) if result else None
        result = reportService.alertLevel(
            report, 'hot', 'hot_temperature', 'hot_temperature')
        self.hotTemperatureAlertLevel = result.get(
            'level', None) if result else None
        result = reportService.alertLevel(
            report, 'hot_flow', 'hot_flow_temperature', 'hot_flow_temperature')
        self.hotFlowTemperatureAlertLevel = result.get(
            'level', None) if result else None

        result = reportService.alertLevel(
            report, 'cold', 'cold_chlorine_dioxide', 'chlorine_dioxide')
        self.coldChlorineDioxideAlertLevel = result.get(
            'level') if result else None
        result = reportService.alertLevel(
            report,
            'cold_flow',
            'cold_flow_chlorine_dioxide',
            'chlorine_dioxide')
        self.coldFlowChlorineDioxideAlertLevel = result.get(
            'level') if result else None
        result = reportService.alertLevel(
            report, 'hot', 'hot_chlorine_dioxide', 'chlorine_dioxide')
        self.hotChlorineDioxideAlertLevel = result.get(
            'level') if result else None
        result = reportService.alertLevel(
            report,
            'hot_flow',
            'hot_flow_chlorine_dioxide',
            'chlorine_dioxide')
        self.hotFlowChlorineDioxideAlertLevel = result.get(
            'level') if result else None
