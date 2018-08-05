# -*- coding: utf-8 -*-
from datetime import datetime
from ..report.service import ReportService
from ..report.freeze import ReportFreeze


class SampleRangeFreezeService(object):

    def freeze(self, sample_range):
        reportService = ReportService()

        # recupero tutti i report del sample_range
        param = {}
        param['sample_range'] = sample_range
        reportList = reportService.getReportListByDict(param)

        reportFreezeList = []
        for report in reportList:
            reportFreeze = ReportFreeze(
                report=report
            )
            reportFreezeList.append(reportFreeze.__dict__)

        freeze_date = datetime.today()

        return freeze_date, reportFreezeList
