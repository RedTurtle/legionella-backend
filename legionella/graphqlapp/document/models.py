# -*- coding: utf-8 -*-
from ..samplerange.models import SampleRange as samplerange_model
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from graphqlapp.utils import upload_to


@python_2_unicode_compatible
class Document(models.Model):
    """ This class describes a Document object: it represents a file to be
    uploaded to the server.
    A SampleRange may have one or more documents attached.
    """
    class Meta:
        verbose_name = "documento"
        verbose_name_plural = "documenti"

    description = models.CharField(max_length=150, blank=False)
    document = models.FileField(upload_to=upload_to)
    samplerange = models.ForeignKey(
        samplerange_model,
        verbose_name='intervallo di campionamento')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "File " + self.description
