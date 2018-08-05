# -*- coding: utf-8 -*-
import graphene
from graphene import relay
from .schema import Floor as FloorSchema
from .mutationservice import FloorMutationService


class CreateFloor(relay.ClientIDMutation):
    """ MUTATION DI PROVA
    """

    class Input:
        # campi che accetto in inserimento
        label = graphene.String(required=True)

    ok = graphene.Boolean()
    floor = graphene.Field(FloorSchema)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        floorMutationService = FloorMutationService()
        piano = floorMutationService.createFloor(input)

        return CreateFloor(floor=piano, ok=bool(piano.id))
