# -*- coding: utf-8 -*-
from .models import Settings as settings_model
from graphene_django import DjangoObjectType

import graphene


class Settings(DjangoObjectType):
    class Meta:
        model = settings_model
        interfaces = (graphene.Node,)
        filter_fields = ['setting_type', 'owner__name']
