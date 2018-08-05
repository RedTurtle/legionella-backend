# -*- coding: utf-8 -*-
import graphene
from graphene_django import DjangoObjectType
from .models import Wsp as wsp_model

# solo per porterli far leggere a graphql
from ..building.schema import Building
from ..sector.schema import Sector

from .service import WspService


class Wsp(DjangoObjectType):
    class Meta:
        model = wsp_model
        interfaces = (graphene.Node, )

    id_db = graphene.ID()
    next_review_date = graphene.String()
    alert_level = graphene.String()
    actions = graphene.String()

    def resolve_id_db(self, info, **input):
        """ Ritorna  l'ID del db """
        return self.id

    def resolve_next_review_date(self, info):
        """
        review_date dell'ultimo Report relativo al WSP
        """
        wspService = WspService()
        return wspService.NextReviewDate(
            wsp=self
        )

    def resolve_alert_level(self, info):
        """
        restituisce il livello di rischio del wsp calcolato dall'ultimo
        rapporto fatto sul quel wsp (sempre per legionella)
        """
        wspService = WspService()
        return wspService.AlertLevel(
            wsp=self
        )

    def resolve_actions(self, info):
        """
        Dovrà prendere le action dell'ultimo Report che è stato fatto
        per questo wsp
        """
        return "TODO"
