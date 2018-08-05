# -*- coding: utf-8 -*-

from graphqlapp.samplerange.models import SampleRange
import datetime


def create_samplerange(self):
    """ Sample Range.
    Aggiunta di intervalli di campionamento.
    """

    if self.flush:
        allSampleRange = SampleRange.objects.all()
        for sample in allSampleRange:
            sample.delete()

    lista = [datetime.date(2017, 4, 15),
             datetime.date(2017, 4, 16),
             datetime.date(2017, 4, 17)]
    sample_manager = SampleRange(
        dates_list=lista,
        company='COMPANY1',
        title='Questo è il titolo del campionamento COMPANY1',
        description='una descrizione',
        filter_on=False,
        manager_block=True,
        final_block=False
    )
    sample_manager.save()

    lista = [datetime.date(2017, 6, 4),
             datetime.date(2017, 6, 5),
             datetime.date(2017, 6, 9)]
    sample_manager = SampleRange(
        dates_list=lista,
        company='COMPANY2',
        title='Anche noi facciamo campionamenti!',
        description='Altra bella descrizione del campionamento',
        filter_on=True,
        manager_block=False,
        final_block=False
    )
    sample_manager.save()

    lista = [datetime.date(2017, 9, 11),
             datetime.date(2017, 9, 18),
             datetime.date(2017, 9, 23)]
    sample_manager = SampleRange(
        dates_list=lista,
        company='COMPANY3',
        title='Campionamento necessario',
        description='speriamo che nulla vada storto',
        filter_on=False,
    )
    sample_manager.save()

    lista = [datetime.date(2017, 10, 11),
             datetime.date(2017, 10, 18),
             datetime.date(2017, 10, 23)]
    sample_manager = SampleRange(
        dates_list=lista,
        company='COMPANY4',
        title='Cerchiamo di campionare',
        description='preleviamo acqua infetta',
        filter_on=False,
    )
    sample_manager.save()
