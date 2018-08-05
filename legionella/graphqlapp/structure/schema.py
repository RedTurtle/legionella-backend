# -*- coding: utf-8 -*-
import graphene
from graphene_django import DjangoObjectType

from .models import Structure as structure_model

from ..graphQL_genericSchema.schema import AlertLevel
from ..wsp.service import WspService

from .service import StructureService


class Structure(DjangoObjectType):
    class Meta:
        model = structure_model
        interfaces = (graphene.Node,)
        filter_fields = ['struct_type__value']

    structure_id = graphene.ID()
    structure_type = graphene.String()
    aggregatedWsps = graphene.Int()

    aggregatedSamplesCold = graphene.Int()
    aggregatedSamplesHot = graphene.Int()

    aggregatedActions = graphene.Int()

    alertLevel = graphene.Field(AlertLevel)

    # id del db
    def resolve_structure_id(self, info, **kwargs):
        return self.id

    # tipo della structure
    def resolve_structure_type(self, info, **kwargs):
        return self.struct_type.value

    # numero di wsp per structure
    def resolve_aggregatedWsps(self, info, **kwargs):
        wspService = WspService()
        param = {}
        param['structure'] = self
        return len(wspService.getWspListByDict(param))

    # numero di campionamenti per acqua fredda
    def resolve_aggregatedSamplesCold(self, info, **kwargs):
        structureService = StructureService()
        return structureService.aggregatedSamplesCold(
            structure=self
        )

    # numero di campionamenti per acqua calda
    def resolve_aggregatedSamplesHot(self, info, **kwargs):
        structureService = StructureService()
        return structureService.aggregatedSamplesHot(
            structure=self
        )

    def resolve_alertLevel(self, info, **kwargs):
        """
        Percentuali di ufcl in acqua fredda per ogni valore di gravità
        """
        structureService = StructureService()
        return structureService.alertLevel(
            structure=self
        )
