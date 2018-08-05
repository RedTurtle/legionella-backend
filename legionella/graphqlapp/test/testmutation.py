# -*- coding: utf-8 -*-
from .tests import populatedb_for_testing
from django.test import TestCase
from graphene.test import Client as GClient
from graphqlapp.schema import schema
from graphqlapp.test import testmutationstrings


class GraphQLMutationTest(TestCase):
    """ Test per le query base di GrapQL
    """

    def setUp(self):
        """
        Excecuted at the very start of the test suite.
        """
        populatedb_for_testing()

    def test_fakeTest(self):
        """
        """

        self.assertTrue(
            True,
            True)
