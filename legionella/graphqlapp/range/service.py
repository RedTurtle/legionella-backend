# -*- coding: utf-8 -*-
from .models import Range as range_model


class RangeService(object):

    def getRangeListByDict(self, param=None):
        """
        restituisce un lista di Range
        input:
            param: dict con i filtri di ricerca
        output:
            list: lista di Range
        """
        return range_model.objects.filter(
            **param
        )
