# -*- coding: utf-8 -*-

import graphene
from graphene_django import DjangoObjectType

from .models import Floor as floor_model


class Floor(DjangoObjectType):
    class Meta:
        model = floor_model
        interfaces = (graphene.Node,)
