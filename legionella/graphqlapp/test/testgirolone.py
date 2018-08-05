# -*- coding: utf-8 -*-

from .tests import populatedb_for_testing
from django.test import TestCase
from graphene.test import Client as GClient
from graphqlapp.schema import schema
from graphqlapp.test import girolonequerystrings


class GiroloneQueryTest(TestCase):
    """ Test per le query del girolone!
    """

    def setUp(self):
        """
        Excecuted at the very start of the test suite.
        """
        populatedb_for_testing()

    def test_chartQueryFiltered1(self):
        """
        """
        client = GClient(schema)
        executed = client.execute(girolonequerystrings.chartQuery1)

        # Questa query comprende UN SOLO intervallo di campionamento.
        # In questo intervallo c'è UN SOLO rapporto, relativo ad un Wsp dentro
        # a una torre.
        # Torre -> quindi viene preso in considerazione solo il campionamento
        #          di acqua fredda scorrimento.

        self.assertEqual(
            executed['data']['chart']['coldChart']['totalCount'],
            1,
            "Numero totale di campionamenti restituito: sbagliato.")

    def test_chartQueryFiltered2(self):
        """ Con questo test controlliamo che nella query del girolone venga
        restituita corretta la percetuale di wsp che sono stati analizzati nel
        periodo di tempo specificato.

        Filtriamo per tipo di struttura: TORRE.
        Vengono controllati solo i WSP che prevedono il campionamento di acqua
        fredda scorrimento.

        Deve uscire il 14% perchè è 1 wsp su un totale di 7.
        """
        client = GClient(schema)
        executed = client.execute(girolonequerystrings.chartQuery2)

        self.assertEqual(
            executed['data']['chart']['coldChart']['wspsPercentage'],
            14,
            "TODO - Percentuale di wspsPercentage restituita sbagliato. "
            "CALCOLARE CON FILTRO TIPO STRUTTURA (expected failure)")
