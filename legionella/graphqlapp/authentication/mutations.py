# -*- coding: utf-8 -*-
import graphene
from graphene import relay
from rest_framework_jwt.serializers import (JSONWebTokenSerializer,
                                            RefreshJSONWebTokenSerializer)
from graphql import GraphQLError
from .schema import User
# from .serializers import PasswordResetConfirmRetypeSerializer
# from .utils import send_password_reset_email


# class ResetPasswordConfirm(relay.ClientIDMutation):
#     """
#     Mutation for requesting a password reset email
#     """
#
#     class Input:
#         uid = graphene.String(required=True)
#         token = graphene.String(required=True)
#         email = graphene.String(required=True)
#         new_password = graphene.String(required=True)
#         re_new_password = graphene.String(required=True)
#
#     success = graphene.Boolean()
#     errors = graphene.List(graphene.String)
#
#     @classmethod
#     def mutate_and_get_payload(cls, root, info, **input):
#         serializer = PasswordResetConfirmRetypeSerializer(data=input)
#         if serializer.is_valid():
#             serializer.user.set_password(serializer.data['new_password'])
#             serializer.user.save()
#             return ResetPasswordConfirm(success=True, errors=None)
#         else:
#             return ResetPasswordConfirm(
#                 success=False, errors=[serializer.errors])


# manda la mail per resettare la password
class ResetPassword(relay.ClientIDMutation):
    """
    Mutation for requesting a password reset email
    """

    class Input:
        email = graphene.String(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            user = User.objects.get(email=input.get('user'))
            send_password_reset_email(context, user)
            return ResetPassword(success=True)
        except:
            return ResetPassword(success=True)


class RefreshToken(relay.ClientIDMutation):
    """
    Mutation to reauthenticate a user
    """
    class Input:
        token = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    token = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        serializer = RefreshJSONWebTokenSerializer(data=input)
        if serializer.is_valid():
            return RefreshToken(
                success=True,
                token=serializer.object['token'],
                errors=None
            )
        else:
            raise GraphQLError(
                u'Non è possibile fare il refresh del '
                + u'token con le credenziali fornite.'
            )


class Login(relay.ClientIDMutation):
    """
    Mutation to login a user
    """
    class Input:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    token = graphene.String()
    user = graphene.Field(User)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        user = {'email': input['email'], 'password': input['password']}
        serializer = JSONWebTokenSerializer(data=user)
        if serializer.is_valid():
            token = serializer.object['token']
            user = serializer.object['user']
            return Login(success=True, user=user, token=token, errors=None)
        else:
            return Login(
                success=False,
                token=None,
                errors=[
                    'email',
                    u'Non è possibile eseguire il login con le '
                    u'credenzili fornite.']
            )
