# -*- coding: utf-8 -*-
from django_filters import FilterSet, OrderingFilter
from .models import Settings as settings_model


class SettingsFilter(FilterSet):
    class Meta:
        model = settings_model
        fields = ['setting_type', 'owner__name']

    order_by = OrderingFilter(
        fields=(
            ('position', 'position'),
            ('value', 'value')
        )
    )
