# -*- coding: utf-8 -*-
from django.test import TestCase
from .tests import populatedb_for_testing


class GoodAuthenticationTest(TestCase):
    """ Questo test controlla che l'autenticazione
    """

    def setUp(self):
        """
        Excecuted at the very start of the test suite.
        """
        populatedb_for_testing()

    def test_can_login_manager(self):
        """
        Testa l'accesso con la vista di login con un account
        """
        response = self.client.post(
            '/graphqlapp/login',
            data={
                'email': 'admin@admin.it',
                'password': 'adminpassword'
            })
        self.assertIn('token', response.content.decode())

    def test_refresh_token(self):
        """
        Testa che un token creato possa essere refreshato (quindi testa
        la vista di refresh).
        """
        response = self.client.post(
            '/graphqlapp/login',
            data={
                'email': 'admin@admin.it',
                'password': 'adminpassword'
            })
        self.assertIn('token', response.content.decode())

        token = response.data['token']

        response = self.client.post(
            '/graphqlapp/refresh-token',
            data={
                'token': token,
            },
        )
        self.assertIn('token', response.content.decode())


class WrongAuthenticationTest(TestCase):
    """ Questo test controlla che l'autenticazione fallisca (perchè si tenta
    di accedere con credenziali sbagliate)
    """

    def setUp(self):
        """
        Excecuted at the very start of the test suite.
        """
        populatedb_for_testing()

    def test_wrong_login(self):
        """
        Testa l'accesso con credenziali sbagliate
        """
        response = self.client.post(
            '/graphqlapp/login',
            data={
                'email': 'foo',
                'password': 'bar'
            })

        status = response.status_code
        self.assertEqual(
            status,
            400,
            u"Un login sbagliato deve restituire 400 e non {}".format(status)
        )
        self.assertIn(
            'Impossibile eseguire il login',
            response.content.decode())
