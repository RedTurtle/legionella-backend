# -*- coding: utf-8 -*-
from graphql_relay.node.node import to_global_id
from ..report_overlay.schema import ReportOverlay, ReportOverlayTemps

import graphene


class GenericAlertLevel(graphene.Interface):
    perfect = graphene.Int()
    good = graphene.Int()
    bad = graphene.Int()
    danger = graphene.Int()
    critical = graphene.Int()


class ReportWorstState(graphene.ObjectType):

    worstStateCold = graphene.String()
    worstStateHot = graphene.String()
    worstStateColdFlow = graphene.String()
    worstStateHotFlow = graphene.String()

    absoluteWorstState = graphene.String()


class AlertLevelHot(graphene.ObjectType):

    class Meta:
        interfaces = (GenericAlertLevel, )

    def __init__(self):
        self.perfect = 0
        self.good = 0
        self.bad = 0
        self.danger = 0
        self.critical = 0


class AlertLevelCold(graphene.ObjectType):

    class Meta:
        interfaces = (GenericAlertLevel, )

    def __init__(self):
        self.perfect = 0
        self.good = 0
        self.bad = 0
        self.danger = 0
        self.critical = 0


class DangerLevel(graphene.ObjectType):

    class Meta:
        interfaces = (GenericAlertLevel, )

    def __init__(self):
        self.perfect = 0
        self.good = 0
        self.bad = 0
        self.danger = 0
        self.critical = 0

    def reset(self):
        self.perfect = 0
        self.good = 0
        self.bad = 0
        self.danger = 0
        self.critical = 0

    def copy(self):
        newone = type(self)()
        newone.__dict__.update(self.__dict__)
        return newone


class DangerLevelTemps(graphene.ObjectType):

    cold_temperature = graphene.Field(DangerLevel)
    cold_flow_temperature = graphene.Field(DangerLevel)
    hot_temperature = graphene.Field(DangerLevel)
    hot_flow_temperature = graphene.Field(DangerLevel)

    def __init__(self):
        self.cold_temperature = DangerLevel()
        self.cold_flow_temperature = DangerLevel()
        self.hot_temperature = DangerLevel()
        self.hot_flow_temperature = DangerLevel()


class AggregatedStructures(graphene.ObjectType):

    structure_id = graphene.ID()
    structure_global_id = graphene.String()
    structure_label = graphene.String()
    structure_type = graphene.String()

    wsps_percentage = graphene.Int()
    wsps_num = graphene.Int()

    samples_num_cold = graphene.Int()
    samples_num_hot = graphene.Int()

    # AGGREGATI
    aggregatedTemps = graphene.Field(DangerLevelTemps)

    aggregatedBioxCold = graphene.Field(AlertLevelCold)
    aggregatedBioxHot = graphene.Field(AlertLevelHot)

    aggregatedLegionellaCold = graphene.Field(AlertLevelCold)
    aggregatedLegionellaHot = graphene.Field(AlertLevelHot)

    # OVERLAY
    overlayLegionellaHot = graphene.Field(ReportOverlay)
    overlayLegionellaCold = graphene.Field(ReportOverlay)
    overlayBioxHot = graphene.Field(ReportOverlay)
    overlayBioxCold = graphene.Field(ReportOverlay)
    overlayTemps = graphene.Field(ReportOverlayTemps)

    def __init__(self, sampleRangeService, sample_range, wspList, structure):

        self.sampleRangeService = sampleRangeService
        self.sample_range = sample_range
        self.wspList = wspList
        self.structure = structure

    def resolve_structure_id(self, info, **input):
        return self.structure.id

    def resolve_structure_global_id(self, info, **input):
        return to_global_id(
            "Structure", self.structure.id)

    def resolve_structure_label(self, info, **input):
        return self.structure.label

    def resolve_structure_type(self, info, **input):
        return self.structure.struct_type.value

    def resolve_wsps_num(self, info, **input):
        return self.sampleRangeService.wspsNum(
            sample_range=self.sample_range,
            wspList=self.wspList
        )

    def resolve_wsps_percentage(self, info, **input):
        return self.sampleRangeService.wspsPercentage(
            sample_range=self.sample_range,
            wspList=self.wspList,
            structure=self.structure
        )

    def resolve_samples_num_cold(self, info, **input):
        return self.sampleRangeService.samplesNumCold(
            sample_range=self.sample_range,
            structure=self.structure,
            wspList=self.wspList
        )

    def resolve_samples_num_hot(self, info, **input):
        return self.sampleRangeService.samplesNumHot(
            sample_range=self.sample_range,
            structure=self.structure,
            wspList=self.wspList
        )

    def resolve_aggregatedBioxHot(self, info, **input):
        return self.sampleRangeService.aggregatedBioxHot(
            sample_range=self.sample_range,
            structure=self.structure,
            wspList=self.wspList
        )

    def resolve_aggregatedBioxCold(self, info, **input):
        return self.sampleRangeService.aggregatedBioxCold(
            sample_range=self.sample_range,
            structure=self.structure,
            wspList=self.wspList
        )

    def resolve_aggregatedLegionellaHot(self, info, **input):
        return self.sampleRangeService.aggregatedLegionellaHot(
            sample_range=self.sample_range,
            structure=self.structure,
            wspList=self.wspList
        )

    def resolve_aggregatedLegionellaCold(self, info, **input):
        return self.sampleRangeService.aggregatedLegionellaCold(
            sample_range=self.sample_range,
            structure=self.structure,
            wspList=self.wspList
        )

    def resolve_aggregatedTemps(self, info, **input):
        return self.sampleRangeService.aggregatedTemps(
            sample_range=self.sample_range,
            structure=self.structure,
            wspList=self.wspList
        )

    def resolve_overlayLegionellaHot(self, info, **input):
        return self.sampleRangeService.overlayLegionellaHot(
            sample_range=self.sample_range,
            structure=self.structure,
            wspList=self.wspList
        )

    def resolve_overlayLegionellaCold(self, info, **input):
        return self.sampleRangeService.overlayLegionellaCold(
            sample_range=self.sample_range,
            structure=self.structure,
            wspList=self.wspList
        )

    def resolve_overlayBioxHot(self, info, **input):
        return self.sampleRangeService.overlayBioxHot(
            sample_range=self.sample_range,
            structure=self.structure,
            wspList=self.wspList
        )

    def resolve_overlayBioxCold(self, info, **input):
        return self.sampleRangeService.overlayBioxCold(
            sample_range=self.sample_range,
            structure=self.structure,
            wspList=self.wspList
        )

    def resolve_overlayTemps(self, info, **input):
        return self.sampleRangeService.overlayTemps(
            sample_range=self.sample_range,
            structure=self.structure,
            wspList=self.wspList
        )


class AlertLevel(graphene.ObjectType):
    alCold = graphene.Field(AlertLevelCold)
    alHot = graphene.Field(AlertLevelHot)

    def __init__(self):
        self.alCold = AlertLevelCold()
        self.alHot = AlertLevelHot()
