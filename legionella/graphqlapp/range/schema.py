# -*- coding: utf-8 -*-
from graphene_django import DjangoObjectType
from .models import Range as ranges_model

import graphene


class Range(DjangoObjectType):

    class Meta:
        model = ranges_model
        interfaces = (graphene.Node, )
        filter_fields = ['flag']
