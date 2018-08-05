# -*- coding: utf-8 -*-

import graphene
from graphene_django import DjangoObjectType

from .models import Sector as sector_model


class Sector(DjangoObjectType):
    class Meta:
        model = sector_model
        interfaces = (graphene.Node,)
