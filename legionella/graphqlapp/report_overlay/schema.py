# -*- coding: utf-8 -*-
import graphene


class StructOverlay(graphene.ObjectType):

    percentage = graphene.Int()
    wsp_num = graphene.Int()
    alert_level = graphene.String()
    range_level = graphene.List(graphene.String)

    def __init__(self):
        self.percentage = 0
        self.wsp_num = 0
        self.alert_level = ""
        self.range_level = []


class ReportOverlay(graphene.ObjectType):

    perfect = graphene.Field(StructOverlay)
    good = graphene.Field(StructOverlay)
    bad = graphene.Field(StructOverlay)
    danger = graphene.Field(StructOverlay)
    critical = graphene.Field(StructOverlay)

    def __init__(self):
        self.perfect = StructOverlay()
        self.good = StructOverlay()
        self.bad = StructOverlay()
        self.danger = StructOverlay()
        self.critical = StructOverlay()


class ReportOverlayTemps(graphene.ObjectType):

    cold_temperature = graphene.Field(ReportOverlay)
    cold_flow_temperature = graphene.Field(ReportOverlay)
    hot_temperature = graphene.Field(ReportOverlay)
    hot_flow_temperature = graphene.Field(ReportOverlay)

    def __init__(self):
        self.cold_temperature = ReportOverlay()
        self.cold_flow_temperature = ReportOverlay()
        self.hot_temperature = ReportOverlay()
        self.hot_flow_temperature = ReportOverlay()
