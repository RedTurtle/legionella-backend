# -*- coding: utf-8 -*-
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from graphqlapp import logger
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.request import Request
from django.conf import settings
import logging

hdlr = logging.FileHandler(settings.LOGGER_FILE_HANDLER)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(hdlr)


class JWTAuthenticationMiddleware(object):
    """ Middleware for authenticating JSON Web Tokens in Authorize Header """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if not request.user.is_authenticated:  # adminsite user
            user = None
            user_jwt = request.META.get('HTTP_AUTHORIZATION', '').split()

            if len(user_jwt) == 2 and user_jwt[0].lower() == 'jwt':
                # token presente
                try:
                    user = JSONWebTokenAuthentication(
                    ).authenticate(Request(request))[0]
                except Exception as err:
                    return JsonResponse({
                        'errors': [{
                            'message': err.detail,
                            'status': err.status_code
                        }]
                    }, status=err.status_code)

                # controllo se l'utente si è autenticato
                if user is not None:
                    request.user = user

            else:
                request.user = AnonymousUser()

        response = self.get_response(request)
        return response
