# -*- coding: utf-8 -*-

from django.db.models import Q
from django.utils import timezone
from graphqlapp.range.models import Range
from graphqlapp.report.models import Report
from graphqlapp.samplerange.models import SampleRange
from graphqlapp.settings.models import Settings
from graphqlapp.wsp.models import Wsp
import datetime


def create_reports(self):
    """ This method creates some Reports.
    """

    if self.flush:
        allReports = Report.objects.all()
        for report in allReports:
            report.delete()

    # report in un sample range senza filtro
    nuovo_report = Report(
        sample_range=SampleRange.objects.get(
            company='COMPANY1'
        ),
        wsp=Wsp.objects.get(
            code='T1.1'
        ),
        rangesettings=Range.objects.get(
            range_type__value='torre'
        ),
        sampling_date=datetime.date(2017, 4, 17),
        # cold_ufcl=,
        cold_flow_ufcl=260,
        hot_ufcl=75,
        hot_flow_ufcl=34,

        # cold_ufcl_sampling_selection=Setting.objects.get(
        #     Q(),
        #     Q()
        # ),
        cold_flow_ufcl_sampling_selection=Settings.objects.get(
            Q(setting_type='sampling_value'),
            Q(value='> 100')
        ),
        # hot_ufcl_sampling_selection=Settings.objects.get(
        #     Q(setting_type='sampling_value'),
        #     Q(value='≤ 100')
        # ),
        # hot_flow_ufcl_sampling_selection=Settings.objects.get(
        #     Q(setting_type='sampling_value'),
        #     Q(value='≤ 50')
        # ),

        # cold_ufcl_type='',
        cold_flow_ufcl_type=Settings.objects.get(
            Q(setting_type='legionella'),
            Q(value='L. adelaidensis')
        ),
        # hot_ufcl_type='',
        # hot_flow_ufcl_type='',
        notes_actions=[],
        # notes_actions=Settings.objects.get(
        #     Q(setting_type='noteaction'),
        #     Q(value='> 100')
        # ).notes_actions_json,

        # after_sampling_status=''
        review_date=datetime.date(2018, 6, 3),

        # cold_temperature=2,
        cold_flow_temperature=6,
        hot_temperature=34,
        hot_flow_temperature=31,

        # cold_chlorine_dioxide=0.15,
        cold_flow_chlorine_dioxide=0.15,
        hot_chlorine_dioxide=0.15,
        hot_flow_chlorine_dioxide=0.15,
    )
    nuovo_report.save()

    # Report 2
    nuovo_report = Report(
        sample_range=SampleRange.objects.get(
            company='COMPANY2'
        ),
        wsp=Wsp.objects.get(
            code='T2.2'
        ),
        rangesettings=Range.objects.get(
            range_type__value='torre'
        ),
        sampling_date=datetime.date(2017, 6, 4),
        # cold_ufcl=,
        cold_flow_ufcl=120,
        hot_ufcl=130,
        # hot_flow_ufcl=34,

        # cold_ufcl_sampling_selection=Setting.objects.get(
        #     Q(),
        #     Q()
        # ),
        cold_flow_ufcl_sampling_selection=Settings.objects.get(
            Q(setting_type='sampling_value'),
            Q(value='> 100')
        ),
        hot_ufcl_sampling_selection=Settings.objects.get(
            Q(setting_type='sampling_value'),
            Q(value='> 100')
        ),
        # hot_flow_ufcl_sampling_selection=Settings.objects.get(
        #     Q(setting_type='sampling_value'),
        #     Q(value='≤ 50')
        # ),

        # cold_ufcl_type='',
        cold_flow_ufcl_type=Settings.objects.get(
            Q(setting_type='legionella'),
            Q(value='L. drancourtil')
        ),
        hot_ufcl_type=Settings.objects.get(
            Q(setting_type='legionella'),
            Q(value='L. cardiaca')
        ),
        # hot_flow_ufcl_type='',
        notes_actions=[],
        # notes_actions=Settings.objects.get(
        #     Q(setting_type='noteaction'),
        #     Q(value='> 100')
        # ).notes_actions_json,

        # after_sampling_status=''
        review_date=datetime.date(2017, 12, 22),

        # cold_temperature=2,
        cold_flow_temperature=6,
        hot_temperature=34,
        # hot_flow_temperature=31,

        # cold_chlorine_dioxide=0.15,
        cold_flow_chlorine_dioxide=0.15,
        hot_chlorine_dioxide=0.15,
        # hot_flow_chlorine_dioxide=0.15,
    )
    nuovo_report.save()

    # Report 3
    nuovo_report = Report(
        sample_range=SampleRange.objects.get(
            company='COMPANY3'
        ),
        wsp=Wsp.objects.get(
            code='2.2'
        ),
        rangesettings=Range.objects.get(
            range_type__value='sottocentrale'
        ),
        sampling_date=datetime.date(2017, 9, 18),
        cold_ufcl=99,
        cold_flow_ufcl=260,
        hot_ufcl=165,
        hot_flow_ufcl=32,

        cold_ufcl_sampling_selection=Settings.objects.get(
            Q(setting_type='sampling_value'),
            Q(value='≤ 100')
        ),
        cold_flow_ufcl_sampling_selection=Settings.objects.get(
            Q(setting_type='sampling_value'),
            Q(value='> 100')
        ),
        hot_ufcl_sampling_selection=Settings.objects.get(
            Q(setting_type='sampling_value'),
            Q(value='> 100')
        ),
        hot_flow_ufcl_sampling_selection=Settings.objects.get(
            Q(setting_type='sampling_value'),
            Q(value='≤ 50')
        ),

        # cold_ufcl_type='',
        cold_flow_ufcl_type=Settings.objects.get(
            Q(setting_type='legionella'),
            Q(value='L. drancourtil')
        ),
        hot_ufcl_type=Settings.objects.get(
            Q(setting_type='legionella'),
            Q(value='L. drozanskil')
        ),
        # hot_flow_ufcl_type='',
        notes_actions=[],
        # notes_actions=Settings.objects.get(
        #     Q(setting_type='noteaction'),
        #     Q(value='> 100')
        # ).notes_actions_json,

        # after_sampling_status=''
        review_date=datetime.date(2018, 2, 18),

        cold_temperature=3.4,
        cold_flow_temperature=9.6,
        hot_temperature=41.2,
        hot_flow_temperature=31,

        cold_chlorine_dioxide=0.15,
        cold_flow_chlorine_dioxide=0.55,
        hot_chlorine_dioxide=0.6,
        hot_flow_chlorine_dioxide=1.5,
    )
    nuovo_report.save()

    # Report 4
    nuovo_report = Report(
        sample_range=SampleRange.objects.get(
            company='COMPANY4'
        ),
        wsp=Wsp.objects.get(
            code='I1'
        ),
        rangesettings=Range.objects.get(
            range_type__value='ingresso'
        ),
        sampling_date=datetime.date(2017, 10, 18),
        # cold_ufcl=99,
        cold_flow_ufcl=60,
        # hot_ufcl=165,
        # hot_flow_ufcl=32,

        # cold_ufcl_sampling_selection=Settings.objects.get(
        #     Q(setting_type='sampling_value'),
        #     Q(value='≤ 100')
        # ),
        cold_flow_ufcl_sampling_selection=Settings.objects.get(
            Q(setting_type='sampling_value'),
            Q(value='≤ 100')
        ),
        # hot_ufcl_sampling_selection=Settings.objects.get(
        #     Q(setting_type='sampling_value'),
        #     Q(value='> 100')
        # ),
        # hot_flow_ufcl_sampling_selection=Settings.objects.get(
        #     Q(setting_type='sampling_value'),
        #     Q(value='≤ 50')
        # ),

        # cold_ufcl_type='',
        cold_flow_ufcl_type=Settings.objects.get(
            Q(setting_type='legionella'),
            Q(value='L. cincinnatiensis')
        ),
        # hot_ufcl_type=Settings.objects.get(
        #     Q(setting_type='legionella'),
        #     Q(value='L. drozanskil')
        # ),
        # hot_flow_ufcl_type='',
        notes_actions=[],
        # notes_actions=Settings.objects.get(
        #     Q(setting_type='noteaction'),
        #     Q(value='> 100')
        # ).notes_actions_json,

        # after_sampling_status=''
        review_date=datetime.date(2018, 3, 11),

        # cold_temperature=3.4,
        cold_flow_temperature=9.6,
        # hot_temperature=41.2,
        # hot_flow_temperature=31,

        # cold_chlorine_dioxide=0.15,
        cold_flow_chlorine_dioxide=0.22,
        # hot_chlorine_dioxide=0.6,
        # hot_flow_chlorine_dioxide=1.5,
    )
    nuovo_report.save()

    # Report 5
    nuovo_report = Report(
        sample_range=SampleRange.objects.get(
            company='COMPANY2'
        ),
        wsp=Wsp.objects.get(
            code='3.9.b'
        ),
        rangesettings=Range.objects.get(
            range_type__value='sottocentrale'
        ),
        sampling_date=datetime.date(2017, 6, 9),
        # cold_ufcl=99,
        # cold_flow_ufcl=60,
        hot_ufcl=365,
        hot_flow_ufcl=5,

        # cold_ufcl_sampling_selection=Settings.objects.get(
        #     Q(setting_type='sampling_value'),
        #     Q(value='≤ 100')
        # ),
        # cold_flow_ufcl_sampling_selection=Settings.objects.get(
        #     Q(setting_type='sampling_value'),
        #     Q(value='≤ 100')
        # ),
        hot_ufcl_sampling_selection=Settings.objects.get(
            Q(setting_type='sampling_value'),
            Q(value='> 100')
        ),
        hot_flow_ufcl_sampling_selection=Settings.objects.get(
            Q(setting_type='sampling_value'),
            Q(value='≤ 50')
        ),

        # cold_ufcl_type='',
        # cold_flow_ufcl_type=Settings.objects.get(
        #     Q(setting_type='legionella'),
        #     Q(value='L. cincinnatiensis')
        # ),
        hot_ufcl_type=Settings.objects.get(
            Q(setting_type='legionella'),
            Q(value='L. beliardensis')
        ),
        # hot_flow_ufcl_type='',
        notes_actions=[],
        # notes_actions=Settings.objects.get(
        #     Q(setting_type='noteaction'),
        #     Q(value='> 100')
        # ).notes_actions_json,

        # after_sampling_status=''
        review_date=datetime.date(2018, 1, 20),

        # cold_temperature=3.4,
        # cold_flow_temperature=9.6,
        hot_temperature=17.1,
        hot_flow_temperature=13,

        # cold_chlorine_dioxide=0.15,
        # cold_flow_chlorine_dioxide=0.22,
        hot_chlorine_dioxide=0.61,
        hot_flow_chlorine_dioxide=0.1,
    )
    nuovo_report.save()

    # Report 6
    nuovo_report = Report(
        sample_range=SampleRange.objects.get(
            company='COMPANY4'
        ),
        wsp=Wsp.objects.get(
            code='4.2'
        ),
        rangesettings=Range.objects.get(
            range_type__value='sottocentrale'
        ),
        sampling_date=datetime.date(2017, 10, 23),
        cold_ufcl=379,
        cold_flow_ufcl=35,
        # hot_ufcl=365,
        # hot_flow_ufcl=5,

        cold_ufcl_sampling_selection=Settings.objects.get(
            Q(setting_type='sampling_value'),
            Q(value='> 100')
        ),
        cold_flow_ufcl_sampling_selection=Settings.objects.get(
            Q(setting_type='sampling_value'),
            Q(value='≤ 50')
        ),
        # hot_ufcl_sampling_selection=Settings.objects.get(
        #     Q(setting_type='sampling_value'),
        #     Q(value='> 100')
        # ),
        # hot_flow_ufcl_sampling_selection=Settings.objects.get(
        #     Q(setting_type='sampling_value'),
        #     Q(value='≤ 50')
        # ),

        cold_ufcl_type=Settings.objects.get(
            Q(setting_type='legionella'),
            Q(value='L. anisa')
        ),
        # cold_flow_ufcl_type=Settings.objects.get(
        #     Q(setting_type='legionella'),
        #     Q(value='L. cincinnatiensis')
        # ),
        # hot_ufcl_type=Settings.objects.get(
        #     Q(setting_type='legionella'),
        #     Q(value='L. beliardensis')
        # ),
        # hot_flow_ufcl_type='',
        notes_actions=[],
        # notes_actions=Settings.objects.get(
        #     Q(setting_type='noteaction'),
        #     Q(value='> 100')
        # ).notes_actions_json,

        # after_sampling_status=''
        review_date=datetime.date(2018, 9, 20),

        cold_temperature=14.4,
        cold_flow_temperature=19.1,
        # hot_temperature=17.1,
        # hot_flow_temperature=13,

        cold_chlorine_dioxide=0.73,
        cold_flow_chlorine_dioxide=0.89,
        # hot_chlorine_dioxide=0.61,
        # hot_flow_chlorine_dioxide=0.1,
    )
    nuovo_report.save()
