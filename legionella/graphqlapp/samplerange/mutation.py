# -*- coding: utf-8 -*-
from __future__ import print_function
from .mutationservice import SampleRangeMutationService
from .schema import SampleRange
from django.db import transaction
from graphene import relay
from graphql import GraphQLError

import graphene


class DeleteSampleRange(relay.ClientIDMutation):
    """ Mutation per la cancellazione di un Intervallo di Campionamento.
    """

    class Input:
        samplerange_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        # controllo se l'utente ha i permessi per aggiungere un report
        if not info.context.user.has_perm('graphqlapp.delete_samplerange'):
            raise GraphQLError(
                u'Non hai i permessi per cancellare un '
                + u'intervallo di campionamento.'
            )

        sampleRangeMutationService = SampleRangeMutationService()
        object_deleted = sampleRangeMutationService.deleteSampleRange(input)

        return DeleteSampleRange(ok=True if object_deleted > 0 else False)


class UpdateSampleRange(relay.ClientIDMutation):
    """ Mutation per effettuare un block/lock di un Intervallo di
    campionamento.
    """

    class Input:
        samplerange_id = graphene.ID(required=True)
        manager_block = graphene.Boolean()
        tecnico_block = graphene.Boolean()
        final_block = graphene.Boolean()

        dates_list = graphene.List(graphene.String)
        company = graphene.String()
        title = graphene.String()
        description = graphene.String()
        filter_on = graphene.Boolean()

    ok = graphene.Boolean()
    sample_range = graphene.Field(SampleRange)

    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **input):

        # CHECK PERMESSI
        # controllo se l'utente ha i permessi per aggiungere un report
        if not info.context.user.has_perm('graphqlapp.change_samplerange'):
            raise GraphQLError(
                u'Non hai i permessi per modificare un '
                + u'intervallo di campionamento.'
            )

        # controllo i permessi dei campi che si vogliono inserire
        for key in input.keys():
            if not info.context.user.has_field_perm('SampleRange', key):
                raise GraphQLError(
                    u'Non hai i permessi per aggiungere questo campo: {0}'.format(
                        key)
                )

        sampleRangeMutationService = SampleRangeMutationService()
        samranobj = sampleRangeMutationService.updateSampleRange(
            input,
            info.context.user.groups.all()
        )

        return UpdateSampleRange(sample_range=samranobj, ok=bool(samranobj))


class CreateSampleRange(relay.ClientIDMutation):
    """ Mutation per la creazione di un Intervallo di Campionamento.
    """

    class Input:
        # Campi che accetto in inserimento.
        # NON prendo anche i vari block perchè questa è la Creazione, quindi
        # NON ci possono essere ancora blocchi di nessun tipo.
        dates_list = graphene.List(graphene.String, required=True)
        company = graphene.String(required=True)
        title = graphene.String(required=True)
        description = graphene.String()
        filter_on = graphene.Boolean(required=True)

    ok = graphene.Boolean()
    samplerange = graphene.Field(SampleRange)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        # controllo se l'utente ha i permessi per aggiungere un report
        if not info.context.user.has_perm('graphqlapp.add_samplerange'):
            raise GraphQLError(
                u'Non hai i permessi per aggiungere un intervallo di campionamento.'
            )

        # controllo i permessi dei campi che si vogliono inserire
        for key in input.keys():
            if not info.context.user.has_field_perm('SampleRange', key):
                raise GraphQLError(
                    u'Non hai i permessi per aggiungere il campo: {0}.'.format(
                        key)
                )

        sampleRangeMutationService = SampleRangeMutationService()
        samplerange = sampleRangeMutationService.createSampleRange(input)

        return CreateSampleRange(
            samplerange=samplerange,
            ok=bool(samplerange)
        )
