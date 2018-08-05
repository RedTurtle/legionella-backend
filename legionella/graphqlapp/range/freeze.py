# -*- coding: utf-8 -*-
from django.forms.models import model_to_dict


class RangeFreeze(object):

    def __init__(self, ranges):
        # mapping di un range in un modello json compatibile
        if ranges.range_type:
            self.range_type = model_to_dict(ranges.range_type)
        if ranges.cold_temperature:
            self.cold_temperature = ranges.cold_temperature
        if ranges.cold_flow_temperature:
            self.cold_flow_temperature = ranges.cold_flow_temperature
        if ranges.hot_temperature:
            self.hot_temperature = ranges.hot_temperature
        if ranges.hot_flow_temperature:
            self.hot_flow_temperature = ranges.hot_flow_temperature
        if ranges.ufcl:
            self.ufcl = ranges.ufcl
        if ranges.chlorine_dioxide:
            self.chlorine_dioxide = ranges.chlorine_dioxide

        # non metto
        # creation_date
        # flag
