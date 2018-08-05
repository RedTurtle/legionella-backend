# -*- coding: utf-8 -*-
import graphene
from graphene_django import DjangoObjectType
from .models import User as UserModel
from django.contrib.auth.models import Group


class Group(DjangoObjectType):
    """
    Gruop Node
    """
    class Meta:
        model = Group
        interfaces = (graphene.Node, )


class User(DjangoObjectType):
    """
    User Node
    """
    class Meta:
        model = UserModel
        filter_fields = {
            'email': ['exact', ]
        }
        exclude_fields = ('password', 'is_superuser', )
        interfaces = (graphene.Node, )

    roles = graphene.List(graphene.String)

    def resolve_roles(self, info, **input):
        roles = []

        for r in self.groups.all():
            roles.append(r.name)

        return roles
