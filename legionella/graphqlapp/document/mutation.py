# -*- coding: utf-8 -*-
from .mutationservice import DocumentMutationService
from .schema import Document  # imported to generate documentSet
from graphql import GraphQLError

import graphene


class DeleteDocument(graphene.ClientIDMutation):

    class Input:
        document_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        # controllo se l'utente ha i permessi per aggiungere un report
        if not info.context.user.has_perm('graphqlapp.delete_document'):
            raise GraphQLError(u'Non hai i permessi per cancellare allegati.')

        documentMutationService = DocumentMutationService()
        object_deleted = documentMutationService.deleteDocument(input)

        return DeleteDocument(ok=True if object_deleted > 0 else False)


class UploadFile(graphene.relay.ClientIDMutation):
    """ Mutation per l'upload di un file come allegato di un intervallo di
    campionamento.
    """

    class Input:
        samplerange_id = graphene.ID(required=True)
        file_description = graphene.String()

    # your return fields
    success = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        documentMutationService = DocumentMutationService()

        # In questo caso, "context" è la nostra request
        files = info.context.FILES
        data = files['file']

        documentMutationService.uploadFile(data, input)

        return UploadFile(success=True)
