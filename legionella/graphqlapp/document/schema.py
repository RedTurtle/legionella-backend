# -*- coding: utf-8 -*-
from graphene_django import DjangoObjectType
from .models import Document as document_model
from graphqlapp.utils import humanbytes

import graphene


class Document(DjangoObjectType):

    class Meta:
        model = document_model
        interfaces = (graphene.Node, )

    documentSizeHuman = graphene.String()
    fileUrl = graphene.String()

    def resolve_fileUrl(self, info, **kwargs):
        return self.document.url

    def resolve_documentSizeHuman(self, info, **kwargs):
        return humanbytes(self.document.size)
