# -*- coding: utf-8 -*-
from .authentication.schema import User
from .chart.schema import ChartContainer
from .document import mutation as documentMutation
from .floor.mutation import CreateFloor
from .range import mutation as RangeMutation
from .range.schema import Range
from .report import mutation as ReportMutation
from .samplerange import mutation as SampleRangeMutation
from .samplerange.schema import SampleRange
from .service import GenericService
from .settings import mutation as SettingsMutation
from .settings.filter import SettingsFilter
from .settings.schema import Settings
from .structure.schema import Structure
from .wsp.schema import Wsp
from graphene_django import DjangoConnectionField, filter

import graphene

# handler = logging.FileHandler(settings.LOGGER_FILE_HANDLER)
# logger.addHandler(handler)


class Query(graphene.ObjectType):
    """ Query entry point graphQL.
    """
    node = graphene.relay.Node.Field()

    # UTENTE LOGGATO
    user = graphene.Field(User)

    # SAMPLERANGES
    # all_sampleRanges = filter.DjangoFilterConnectionField(
    all_sampleRanges = DjangoConnectionField(
        SampleRange,
        startDate=graphene.String(),
        endDate=graphene.String(),
        description="all the sample range"
    )
    sampleRange = graphene.Node.Field(SampleRange)

    # STRUCTURE
    all_structure = filter.DjangoFilterConnectionField(
        Structure,
        description="Filterable list of structure"
    )
    structure = graphene.Node.Field(Structure)

    # NODO GENERICO
    node = graphene.Node.Field()

    # SETTINGS
    settings = filter.DjangoFilterConnectionField(
        Settings,
        filterset_class=SettingsFilter,
        description="Filterable settings values"
    )
    setting = graphene.Node.Field(Settings)

    # WSP
    wsp = graphene.Field(
            Wsp,
            id=graphene.ID(),
        )

    # RANGE / Intevallo di rischio
    all_ranges = filter.DjangoFilterConnectionField(
        Range,
        description="List of all the ranges"
    )
    rangenode = graphene.Node.Field(Range)

    chart = graphene.Field(
        ChartContainer,
        startDate=graphene.String(required=True),
        endDate=graphene.String(required=True),
        struct_type=graphene.String(),
        struct_id=graphene.ID(),
    )

    def resolve_wsp(self, info, **input):
        """ Questo resolve permette di recuperare un Wsp sia con global_id che
        con id del database.
        """
        genericService = GenericService()
        return genericService.Wsp(input=input)

    def resolve_chart(self, info, **input):
        chartContainer = ChartContainer(
            input.get('struct_type', None),
            input.get('startDate', None),
            input.get('endDate', None),
            input.get('struct_id', None),
        )
        return chartContainer

    # torno le informazioni dell'utente LOGGATO
    def resolve_user(self, info, **input):
        return info.context.user

    # torno i samplerange in ordine di data
    def resolve_all_sampleRanges(self, info, **input):
        genericService = GenericService()
        return genericService.allSampleRanges(input=input)

    def resolve_all_structure(self, info, **input):
        genericService = GenericService()
        return genericService.allStructure(input=input)


class Mutation(graphene.ObjectType):
    """ Mutation entry point graphQL.
    """
    # TEST - mutation per Floor: funzionante
    create_floor = CreateFloor.Field()
    # sampleRange
    create_samplerange = SampleRangeMutation.CreateSampleRange.Field()
    delete_samplerange = SampleRangeMutation.DeleteSampleRange.Field()
    update_samplerange = SampleRangeMutation.UpdateSampleRange.Field()
    # report
    create_report = ReportMutation.CreateReport.Field()
    delete_report = ReportMutation.DeleteReport.Field()
    update_report = ReportMutation.UpdateReport.Field()
    # range
    create_range = RangeMutation.CreateRange.Field()
    update_range = RangeMutation.UpdateRange.Field()
    # settings
    create_settings = SettingsMutation.CreateSetting.Field()
    update_setting = SettingsMutation.UpdateSetting.Field()
    delete_setting = SettingsMutation.DeleteSetting.Field()
    # Attachments - Gestione dei file per i SampleRange
    upload_file = documentMutation.UploadFile.Field()
    delete_file = documentMutation.DeleteDocument.Field()


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
