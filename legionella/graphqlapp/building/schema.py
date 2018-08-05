# -*- coding: utf-8 -*-

import graphene
from graphene_django import DjangoObjectType

from .models import Building as building_model


class Building(DjangoObjectType):
    class Meta:
        model = building_model
        interfaces = (graphene.Node,)
