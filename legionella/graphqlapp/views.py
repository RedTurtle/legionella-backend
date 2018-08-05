# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from graphene_django.views import GraphQLView
from graphqlapp.samplerange.service import SampleRangeService
from graphqlapp.utils import create_excel_file


class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    raise_exception = True


def downloadExcel(request):
    """ Crea e restituisce un excel.

    Vengono considerati solo gli intervalli di campionamento validati al 100%.
    Sono necessari due parametri: data di inizio e di fine. Solo gli intervalli
    che ricadono in questa forchetta verranno presi in considerazione.

    Accettiamo sia richieste GET che POST.
    Le due variabili che ci aspettiamo sono 'startDate' e 'endDate'.
    Se una delle due non viene settata, consideriamo il periodo standard degli
    ultimo due anni.
    """

    if request.method == 'GET':
        startDate = request.GET.get('startDate', None)
        endDate = request.GET.get('endDate', None)
    elif request.method == 'POST':
        startDate = request.POST.get('startDate', None)
        endDate = request.POST.get('endDate', None)

    if startDate:
        startDate = datetime.strptime(startDate, "%Y-%m-%d")

    if endDate:
        endDate = datetime.strptime(endDate, "%Y-%m-%d")

    if not startDate or not endDate:
        # Se qualcosa non viene settato, mandiamo il periodo standard
        # degli ultimi due anni da oggi
        endDate = datetime.today()
        startDate = endDate.replace(year=endDate.year - 2)

    sampleRangeService = SampleRangeService()

    samplerange_list = sampleRangeService.getSampleRangeByStartDateAndEndDate(
        endDate=endDate,
        startDate=startDate,
    )

    ordinati = sorted(
        samplerange_list,
        key=lambda samplerange: samplerange.dates_list[0],
        reverse=False,
    )

    # Solo quelli che sono stati VALIDATI COMPLETAMENTE
    filtrati = filter(
        lambda x: x.final_block,
        ordinati,
    )

    # Prepariamoci a servire il file
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Report.xlsx'

    # Creiamo il file vero e proprio
    xlsx_data = create_excel_file(filtrati)
    response.write(xlsx_data)
    return response

    return HttpResponse("""<h3>download excel report</h3>""")
