# -*- coding: utf-8 -*-
from __future__ import print_function
from .mutationservice import SettingsMutationService
from .schema import Settings
from django.db import transaction
from graphene import relay

import graphene


class DeleteSetting(relay.ClientIDMutation):
    """Mutation per la cancellazione di un settaggio (modello: Settings).
    """

    class Input:
        setting_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        settingsMutationService = SettingsMutationService()
        object_deleted = settingsMutationService.deleteSetting(input)

        return DeleteSetting(ok=True if object_deleted > 0 else False)


class UpdateSetting(relay.ClientIDMutation):
    """ Mutation per l'aggiornamento di un settaggio (modello: Settings).
    """

    class Input:
        setting_id = graphene.ID(required=True)
        setting_type = graphene.String(
            description="identificativo del tipo di settaggio"
        )
        value = graphene.String(
            description="il valore del settaggio"
        )
        description = graphene.String()
        notes_actions_json = graphene.String(
            description="JSON da cui prendere le note e le azioni."
        )
        position = graphene.Int(
            description="posizione in cui vogliamo venga restituita la setting"
        )

    ok = graphene.Boolean()
    updatedsetting = graphene.Field(Settings)

    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **input):
        settingsMutationService = SettingsMutationService()
        settingobj = settingsMutationService.updateSetting(input)

        return UpdateSetting(updatedsetting=settingobj, ok=bool(settingobj))


class CreateSetting(relay.ClientIDMutation):
    """ Mutation per la creazione di un settaggio (modello: Settings).
    """

    class Input:
        setting_type = graphene.String(
            required=True,
            description="identificativo del tipo di settaggio")
        value = graphene.String(
            required=True,
            description="il valore del settaggio")
        description = graphene.String()
        notes_actions_json = graphene.String(
            description="JSON da cui prendere le note e le azioni. \n"
            "Da usare solo quando il setting_type è noteaction."
        )
        # `owner` no perchè i permessi non vengono gestiti da GraphQL.
        # Stesso discorso per `has_legionella_type`.

    ok = graphene.Boolean()
    newsetting = graphene.Field(Settings)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        settingsMutationService = SettingsMutationService()
        settings = settingsMutationService.createSetting(input)

        return CreateSetting(
            newsetting=settings,
            ok=bool(settings)
        )
