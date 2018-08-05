# -*- coding: utf-8 -*-
from .mutationservice import RangeMutationService
from .schema import Range
from django.db import transaction
from graphql import GraphQLError

import graphene

# non ci sono metodi di modifica o cancellazione, tutto viene fatto tramite
# l'inserimento di un nuovo range


class UpdateRange(graphene.ClientIDMutation):

    class Input:
        range_id = graphene.ID(required=True)
        range_type = graphene.ID()
        cold_temperature = graphene.String()
        cold_flow_temperature = graphene.String()
        hot_temperature = graphene.String()
        hot_flow_temperature = graphene.String()
        ufcl = graphene.String()
        chlorine_dioxide = graphene.String()

        # l'utente non sceglie quale range è a True
        # quella è una cosa che viene soltanto gestita internamente

    ok = graphene.Boolean()
    ranges = graphene.Field(Range)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        # controllo se l'utente ha i permessi per aggiungere un report
        if not info.context.user.has_perm('graphqlapp.change_range'):
            raise GraphQLError(u"L'utente non ha il permesso di modificare "
                               u"Intervalli di rischio.")

        rangeMutationService = RangeMutationService()
        ranges = rangeMutationService.updateRange(input)

        return UpdateRange(
            ranges=ranges,
            ok=bool(ranges.id)
        )


class CreateRange(graphene.ClientIDMutation):

    class Input:
        range_type = graphene.ID(required=True)
        cold_temperature = graphene.String()
        cold_flow_temperature = graphene.String()
        hot_temperature = graphene.String()
        hot_flow_temperature = graphene.String()
        ufcl = graphene.String()
        chlorine_dioxide = graphene.String()

        # il flag viene inserito automaticamente a True
        # l'unica cosa che dobbiamo fare è assicurarci che quello vecchio
        # sia messo a false

    ok = graphene.Boolean()
    ranges = graphene.Field(Range)

    # la funzione l'ho resa atomica perche se qualcosa va storto
    # durante l'inserimento di un range, voglio che venga ripristinato
    # quello prima

    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **input):

        # controllo se l'utente ha i permessi per aggiungere un report
        if not info.context.user.has_perm('graphqlapp.add_range'):
            raise GraphQLError(u"L'utente non ha il permesso di aggiungere "
                               u"Intervalli di rischio.")

        rangeMutationService = RangeMutationService()
        ranges = rangeMutationService.createRange(input)

        return CreateRange(
            ranges=ranges,
            ok=bool(ranges.id)
        )
