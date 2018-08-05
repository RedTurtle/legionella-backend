# -*- coding: utf-8 -*-

from .tests import populatedb_for_testing
from django.test import TestCase
from graphene.test import Client as GClient
from graphqlapp.schema import schema
from graphqlapp.test import testquerystrings


class GraphQLQueryTest(TestCase):
    """ Test per le query base di GrapQL
    """

    def setUp(self):
        """
        Excecuted at the very start of the test suite.
        """
        populatedb_for_testing()

    def test_allSampleRanges(self):
        """ Recuperiamo tutti gli intervalli di camp.
        """
        client = GClient(schema)
        executed = client.execute(testquerystrings.allSampleranges)

        self.assertEqual(
            executed,
            ({
                "data": {
                    "allSampleranges": {
                        "edges": [
                            {
                                "node": {
                                    "title": u"Cerchiamo di campionare"
                                }
                            },
                            {
                                "node": {
                                    "title": u"Campionamento necessario"
                                }
                            },
                            {
                                "node": {
                                    "title": u"Anche noi facciamo campionamenti!"
                                }
                            },
                            {
                                "node": {
                                    "title": u"Questo è il titolo del campionamento COMPANY1"
                                }
                            }
                        ]
                    }
                }
            }),
            "L'ordine dei sample range restituito non è corretto.")

        self.assertEqual(
            len(executed['data']['allSampleranges']['edges']),
            4)

    def test_firstTwoSampleRanges(self):
        """ Recuperiamo i primi due intervalli di camp.
        (quindi i due più recenti)
        """
        client = GClient(schema)
        executed = client.execute(testquerystrings.firstTwoSampleRanges)

        assert executed == {
            "data": {
                "allSampleranges": {
                    "edges": [
                        {
                            "node": {
                                "title": "Cerchiamo di campionare"
                            }
                        },
                        {
                            "node": {
                                "title": "Campionamento necessario"
                            }
                        }
                    ]
                }
            }
        }

        self.assertEqual(
            len(executed['data']['allSampleranges']['edges']),
            2,
            "Sono stati richiesti due sample range ma il risultato è diverso.")

    def test_allStructure(self):
        """ Recuperiamo tutte le strutture presenti.
        """
        client = GClient(schema)
        executed = client.execute(testquerystrings.allStructure)

        self.assertEqual(
            len(executed['data']['allStructure']['edges']),
            10,
            "Il numero delle strutture restituite non è corretto.")

    def test_allSettings(self):
        """ Recuperiamo tutti i settaggi.
        """
        client = GClient(schema)
        executed = client.execute(testquerystrings.allSettings)

        self.assertNotEqual(
            len(executed['data']['settings']['edges']),
            0,
            "Il numero dei settings restituito non è corretto.")

    def test_numberOfReportForSampleRange(self):
        """ Controlliamo che il numero di rapporti relativi agli intevalli di
        campionamento corrispondano.

        In questo caso li controllo per i primi due (i due più recenti)
        intervalli.

        COMPANY4 ne deve avere due.
        COMPANY3 ne deve avere uno.
        """

        client = GClient(schema)
        executed = client.execute(testquerystrings.reportForSampleRange)

        COMPANY3_report = 0
        COMPANY4_report = 0

        for node in executed['data']['allSampleranges']['edges']:
            if node['node']['company'] == 'COMPANY3':
                COMPANY3_report = len(node['node']['reportSet']['edges'])
            if node['node']['company'] == 'COMPANY4':
                COMPANY4_report = len(node['node']['reportSet']['edges'])

        self.assertEqual(COMPANY3_report, 1)
        self.assertEqual(COMPANY4_report, 2)
