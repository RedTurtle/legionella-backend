# -*- coding: utf-8 -*-
from .mutationservice import ReportMutationService
from .schema import Report
from django.conf import settings
from graphql import GraphQLError
from graphqlapp import logger
import graphene
import logging

hdlr = logging.FileHandler(settings.LOGGER_FILE_HANDLER)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(hdlr)


class DeleteReport(graphene.ClientIDMutation):

    class Input:
        report_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        # controllo se l'utente ha i permessi per aggiungere un report
        if not info.context.user.has_perm('graphqlapp.delete_report'):
            raise GraphQLError(
                u'Non hai i permessi per eliminare ' +
                u'un rapporto di campionemanto.'
            )

        reportMutationService = ReportMutationService()
        object_deleted = reportMutationService.deleteReport(input)

        return DeleteReport(ok=True if object_deleted > 0 else False)


class UpdateReport(graphene.relay.ClientIDMutation):
    """
    Mutations that update a Report
    """

    class Input:
        report_id = graphene.ID(required=True)
        sample_range = graphene.ID(required=True)
        wsp = graphene.ID(required=True)

        sampling_date = graphene.String()

        # UTENTE MANAGER
        cold_ufcl = graphene.Int()
        cold_flow_ufcl = graphene.Int()
        hot_ufcl = graphene.Int()
        hot_flow_ufcl = graphene.Int()

        notes_actions = graphene.String()
        after_sampling_status = graphene.String()
        review_date = graphene.String()

        cold_ufcl_type = graphene.ID()
        cold_flow_ufcl_type = graphene.ID()
        hot_ufcl_type = graphene.ID()
        hot_flow_ufcl_type = graphene.ID()
        cold_ufcl_sampling_selection = graphene.ID()
        cold_flow_ufcl_sampling_selection = graphene.ID()
        hot_ufcl_sampling_selection = graphene.ID()
        hot_flow_ufcl_sampling_selection = graphene.ID()

        # UTENTE TECNICO
        cold_temperature = graphene.Float()
        cold_flow_temperature = graphene.Float()
        hot_temperature = graphene.Float()
        hot_flow_temperature = graphene.Float()

        cold_chlorine_dioxide = graphene.Float()
        cold_flow_chlorine_dioxide = graphene.Float()
        hot_chlorine_dioxide = graphene.Float()
        hot_flow_chlorine_dioxide = graphene.Float()

    ok = graphene.Boolean()
    report = graphene.Field(Report)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        # CHECK PERMESSI
        # controllo se l'utente ha i permessi per aggiungere un report
        if not info.context.user.has_perm('graphqlapp.change_report'):
            raise GraphQLError(
                u'Non hai i permessi per modificare ' +
                u'un rapporto di campionamento.'
            )

        # controllo i permessi dei campi che si vogliono inserire
        for key in input.keys():
            if not info.context.user.has_field_perm('Report', key):
                return GraphQLError(
                    u'Non hai i permessi per aggiungere il campo: {0}.'.format(
                        key)
                )

        reportMutationService = ReportMutationService()
        report = reportMutationService.updateReport(
            input, info.context.user.groups.all())

        return UpdateReport(report=report, ok=bool(report.id),)


class CreateReport(graphene.relay.ClientIDMutation):

    """ Mutation that creates a new report
    """

    class Input:
        sample_range = graphene.ID(required=True)
        wsp = graphene.ID(required=True)

        sampling_date = graphene.String()

        # UTENTE MANAGER
        cold_ufcl = graphene.Int()
        cold_flow_ufcl = graphene.Int()
        hot_ufcl = graphene.Int()
        hot_flow_ufcl = graphene.Int()

        notes_actions = graphene.String()
        after_sampling_status = graphene.String()
        review_date = graphene.String()

        cold_ufcl_type = graphene.ID()
        cold_flow_ufcl_type = graphene.ID()
        hot_ufcl_type = graphene.ID()
        hot_flow_ufcl_type = graphene.ID()
        cold_ufcl_sampling_selection = graphene.ID()
        cold_flow_ufcl_sampling_selection = graphene.ID()
        hot_ufcl_sampling_selection = graphene.ID()
        hot_flow_ufcl_sampling_selection = graphene.ID()

        # UTENTE TECNICO
        cold_temperature = graphene.Float()
        cold_flow_temperature = graphene.Float()
        hot_temperature = graphene.Float()
        hot_flow_temperature = graphene.Float()

        cold_chlorine_dioxide = graphene.Float()
        cold_flow_chlorine_dioxide = graphene.Float()
        hot_chlorine_dioxide = graphene.Float()
        hot_flow_chlorine_dioxide = graphene.Float()

    ok = graphene.Boolean()
    report = graphene.Field(Report)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        # controllo se l'utente ha i permessi per aggiungere un report
        if not info.context.user.has_perm('graphqlapp.add_report'):
            raise GraphQLError(
                u'Non hai i permessi per aggiungere ' +
                u'un nuovo rapporto di campionemanto.'
            )

        # controllo i permessi dei campi che si vogliono inserire
        for key in input.keys():
            if not info.context.user.has_field_perm('Report', key):
                return GraphQLError(
                    u'Non hai i permessi per aggiungere il campo: {0}.'.format(
                        key)
                )

        reportMutationService = ReportMutationService()
        report = reportMutationService.createReport(input)
        return CreateReport(report=report, ok=bool(report.id))
