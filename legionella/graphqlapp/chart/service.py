# -*- coding: utf-8 -*-
from ..report.service import ReportService


class ChartSchemaService(object):

    def chartRangesLevel(self, chart_type, recentReportList, ranges):
        """
        il numero di campionameni divisi per livello di allerta
        input:
            chart_type: dict
                esempio:
                    {'cold': 'cold_ufcl', 'cold_flow': 'cold_flow_ufcl'}
            recentReportList: lista di report
            ranges: ChartRanges
        output:
            ranges: ChartRanges
        """
        reportService = ReportService()
        for rep in recentReportList:
            worstLevel = {}
            for ty in chart_type.keys():
                if getattr(rep.wsp, ty) \
                        and getattr(rep, chart_type[ty]) is not None:
                    al = reportService.alertLevelCalculation(
                        value=getattr(rep, chart_type[ty]),
                        setting=rep.rangesettings.ufcl
                    )
                    if al:
                        if not worstLevel \
                                or worstLevel['priority'] > al['priority']:
                            worstLevel['priority'] = al['priority']
                            worstLevel['level'] = al['level']
            if worstLevel:
                setattr(ranges, worstLevel['level'], getattr(
                    ranges, worstLevel['level']) + 1)
        return ranges
