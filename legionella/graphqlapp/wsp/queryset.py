# -*- coding: utf-8 -*-
import operator
from django.db.models.query import QuerySet
from django.db.models import Q


class MyQuerySet(QuerySet):
    def dynamic_or(self, **kwargs):
        or_statements = []
        for key, value in kwargs.items():
            or_statements.append(Q(**{key: value}))

        return self.filter(reduce(operator.or_, or_statements))
