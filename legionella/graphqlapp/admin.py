# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from .authentication.models import User
from .building.models import Building
from .document.models import Document
from .floor.models import Floor
from .forms import CustomUserChangeForm, CustomUserForm
from .range.models import Range
from .report.models import Report
from .samplerange.models import SampleRange
from .sector.models import Sector
from .settings.models import Settings
from .structure.models import Structure
from .wsp.models import Wsp
from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from graphqlapp import logger
from graphqlapp.utils import get_model_admin_perms

import logging
import operator

hdlr = logging.FileHandler(settings.LOGGER_FILE_HANDLER)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(hdlr)

# Custom admin-site
# Text to put in each page's <h1> (and above login form).
admin.site.site_header = 'Legionella'
# Text to put at the end of each page's <title>.
admin.site.site_title = 'Amministrazione applicativo'
# Text to put at the top of the admin index page.
admin.site.index_title = 'Amministrazione Legionella'

# Lista dei modelli da mostrare nell'admin-backend di Django

admin.site.register(Floor)

# #################
# PERSONALIZZAZIONE DELLE VISTE DEI MODELLI NELL'ADMIN SITE
# #################


class RangeForm(forms.ModelForm):
    """ ModelForm per il modello Range
    """
    class Meta:
        model = Range
        exclude = []

    range_type = forms.models.ModelChoiceField(
        queryset=Settings.objects.filter(
            setting_type='struct_type',
        ),
    )


class RangeAdmin(admin.ModelAdmin):
    """ Modello per l'admin site relativo a Range.
    Ci serve per filtrare i settings nella select.
    """

    def get_form(self, request, obj=None, **kwargs):
        return RangeForm

    def get_model_perms(self, request):
        if get_model_admin_perms(request, 'Range'):
            return super(RangeAdmin, self).get_model_perms(request)
        else:
            return {}


admin.site.register(Range, RangeAdmin)


class DocumentForm(forms.ModelForm):
    """ ModelForm per il modello Wsp
    """
    class Meta:
        model = Document
        exclude = []


class DocumentAdmin(admin.ModelAdmin):
    """ Modello per l'admin site relativo ad un Documento (allegato).
    """

    def get_form(self, request, obj=None, **kwargs):
        return DocumentForm

    def get_model_perms(self, request):
        if get_model_admin_perms(request, 'Document'):
            return super(DocumentAdmin, self).get_model_perms(request)
        else:
            return {}


admin.site.register(Document, DocumentAdmin)


class SampleRangeAdmin(admin.ModelAdmin):
    """ Modello per l'admin site relativo ad un SampleRange.
    Aggiungiamo un campo per mostrare i documenti/allegati relativi a quel
    sample range.
    """
    readonly_fields = ('attachments',)

    def attachments(self, instance):
        docs = instance.document_set.all()
        html_string = format_html_join(
            mark_safe('<br/>'),
            '{}',
            ((doc.description,) for doc in docs),
        ) or mark_safe("<span class='errors'>Nessun documento.</span>")
        return html_string

    def get_model_perms(self, request):
        if get_model_admin_perms(request, 'SampleRange'):
            return super(SampleRangeAdmin, self).get_model_perms(request)
        else:
            return {}

    attachments.short_description = "Documenti allegati"


admin.site.register(SampleRange, SampleRangeAdmin)


class WspForm(forms.ModelForm):
    """ ModelForm per il modello Wsp
    """
    class Meta:
        model = Wsp
        exclude = []

    risk_level = forms.models.ModelChoiceField(
        queryset=Settings.objects.filter(
            setting_type='risk_level',
        ),
        label='Livello di rischio',
    )

    building = forms.models.ModelChoiceField(
        queryset=Building.objects.all().order_by('label'),
        label='Edificio',
    )

    sector = forms.models.ModelMultipleChoiceField(
        queryset=Sector.objects.all().order_by('label'),
        label='Settore',
    )


class WspAdmin(admin.ModelAdmin):
    """ Modello per l'admin site relativo a Wsp.
    Ci serve per filtrare i settings per la select del risk_level.
    In più, abilitiamo la ricerca su alcuni campi.
    """
    search_fields = ['code', 'old_name', 'description']
    list_display = ('wsp_str', 'structure', 'building', 'operative_status')

    def get_form(self, request, obj=None, **kwargs):
        return WspForm

    def wsp_str(self, instance):
        return instance.__str__()

    def get_model_perms(self, request):
        if get_model_admin_perms(request, 'Wsp'):
            return super(WspAdmin, self).get_model_perms(request)
        else:
            return {}


admin.site.register(Wsp, WspAdmin)


class StructureForm(forms.ModelForm):
    """ ModelForm per il modello Structure
    """
    class Meta:
        model = Structure
        exclude = []

    struct_type = forms.models.ModelChoiceField(
        queryset=Settings.objects.filter(
            setting_type='struct_type',
        ),
        label='Tipo di struttura',
    )


class StructureAdmin(admin.ModelAdmin):
    """ Modello per l'admin site relativo a Structure.
    Ci serve per filtrare i settings per tipo di impianto.
    """

    def get_form(self, request, obj=None, **kwargs):
        return StructureForm

    def get_model_perms(self, request):
        if get_model_admin_perms(request, 'Structure'):
            return super(StructureAdmin, self).get_model_perms(request)
        else:
            return {}


admin.site.register(Structure, StructureAdmin)


class BuildingAdmin(admin.ModelAdmin):
    """ Modello per l'admin site relativo a Building.
    Abilitiamo la ricerca su alcuni campi.
    """
    search_fields = ['label']
    list_display = ('edificio', 'structure')

    def edificio(self, instance):
        return instance.__str__()

    def get_model_perms(self, request):
        if get_model_admin_perms(request, 'Building'):
            return super(BuildingAdmin, self).get_model_perms(request)
        else:
            return {}


admin.site.register(Building, BuildingAdmin)


class SectorAdmin(admin.ModelAdmin):
    """ Modello per l'admin site relativo a Sector.
    Abilitiamo la ricerca su alcuni campi.
    """
    search_fields = ['label', 'description']
    list_display = ('settore', 'label', 'description')

    def settore(self, instance):
        return instance.__str__()

    def get_model_perms(self, request):
        if get_model_admin_perms(request, 'Sector'):
            return super(SectorAdmin, self).get_model_perms(request)
        else:
            return {}


admin.site.register(Sector, SectorAdmin)


class SettingsAdmin(admin.ModelAdmin):
    """ Modello per l'admin site relativo ai Settings.
    """
    def get_model_perms(self, request):
        if get_model_admin_perms(request, 'Settings'):
            return super(SettingsAdmin, self).get_model_perms(request)
        else:
            return {}


admin.site.register(Settings, SettingsAdmin)


class ReportAdmin(admin.ModelAdmin):
    """ Modello per l'admin site relativo ai Settings.
    """
    def get_model_perms(self, request):
        if get_model_admin_perms(request, 'Report'):
            return super(ReportAdmin, self).get_model_perms(request)
        else:
            return {}


admin.site.register(Report, ReportAdmin)


# New entry for the user to mimic the usual look of the normal user
# Very important! Without this and the custom forms, the user management logic
# is totally broken.
class CustomUserAdmin(UserAdmin):
    """ Necessario per modificare le varie istanze degli utenti
    dall'admin di django (visto che abbiamo modificato l'utente base)
    """

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )

    form = CustomUserChangeForm
    add_form = CustomUserForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
