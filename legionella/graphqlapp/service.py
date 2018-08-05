# -*- coding: utf-8 -*-
from .samplerange.service import SampleRangeService
from .structure.service import StructureService
from .wsp.service import WspService
from datetime import datetime
from django.utils.timezone import utc


class GenericService(object):

    def Wsp(self, input):
        """ Può recuperare un Wsp sia per global Id che per Id del database.
        """
        wspService = WspService()
        wsp_obj = wspService.getWspById(input)
        return wsp_obj

    # sample ranfe ordinati per data
    def allSampleRanges(self, input):
        samplerange_list = None
        sampleRangeService = SampleRangeService()

        if not input.get('startDate') or not input.get('endDate'):
            # prendo i sample range non piu vecchi di due anni
            # ed in ordine di data
            today = datetime.today()
            today = today.replace(year=today.year - 2)

            param = {'dates_list__0__gte': today.replace(tzinfo=utc)}
            samplerange_list = sampleRangeService.getSampleRangeListByDict(
                param)
        else:
            samplerange_list = sampleRangeService.getSampleRangeByStartDateAndEndDate(
                endDate=input.get('endDate'),
                startDate=input.get('startDate')
            )

        return sorted(
            samplerange_list,
            key=lambda samplerange: samplerange.dates_list[0],
            reverse=True,
        )

    def allStructure(self, input):
        structureService = StructureService()
        structureList = []

        # recupero tutti gli ingressi
        structureList.extend(sorted(structureService.getStructureByType(
            'ingresso'
        ), key=lambda structure: structure.label))
        # recupero tutte le torri
        structureList.extend(sorted(structureService.getStructureByType(
            'torre'
        ), key=lambda structure: structure.label))
        # reupero tutte le sottocentrali
        structureList.extend(sorted(structureService.getStructureByType(
            'sottocentrale'
        ), key=lambda structure: structure.label))

        return structureList
