# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from django.test import TestCase, Client
from graphqlapp.management.commands import populatedb
import logging


# Logging settings
logging.basicConfig(level=logging.INFO)


def populatedb_for_testing():
    populate = populatedb.Command()
    opts = {
        'flush': True,
    }
    populate.handle(**opts)


class BareMinimumPageTest(TestCase):
    """ Questo test controlla che le pagine base rispondano correttamente.
    """

    def setUp(self):
        """
        Excecuted at the very start of the test suite.
        """
        populatedb_for_testing()

    def tearDown(self):
        """
        Metti qui quello che vuoi venga eseguito al termine del test.
        """

    def test_admin_page_responds(self):
        self.client = Client(enforce_csrf_checks=True)

        response = self.client.get("/amministrazione/")
        if isinstance(response, HttpResponseRedirect):
            response = self.client.get(response.url)

        html = response.content.decode('utf8')

        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>Accedi', html)
        self.assertTrue(html.endswith('</html>\n'))
