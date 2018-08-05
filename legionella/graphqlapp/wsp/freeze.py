# -*- coding: utf-8 -*-
from django.forms.models import model_to_dict
from .service import WspService


class WspFreeze(object):

    def __init__(self, wsp):
        # mapping del wsp in un modello json compatibile
        self.id = wsp.id  # ci sono sempre, per forza
        self.pk = wsp.pk  # ci sono sempre, per forza
        if wsp.code:
            self.code = wsp.code
        if wsp.old_name:
            self.old_name = wsp.old_name
        if wsp.description:
            self.description = wsp.description
        if wsp.closed_rooms:
            self.closed_rooms = wsp.closed_rooms
        if wsp.open_rooms:
            self.open_rooms = wsp.open_rooms
        if wsp.risk_level:
            self.risk_level = model_to_dict(wsp.risk_level)
        if wsp.risk_threshold:
            self.risk_threshold = model_to_dict(wsp.risk_threshold)
        if wsp.start_date:
            self.start_date = wsp.start_date.strftime("%Y-%m-%d")
        if wsp.obsolence_date:
            self.obsolence_date = wsp.obsolence_date.strftime("%Y-%m-%d")
        if wsp.operative_status:
            self.operative_status = wsp.operative_status
        if wsp.cold:
            self.cold = wsp.cold
        if wsp.cold_flow:
            self.cold_flow = wsp.cold_flow
        if wsp.hot:
            self.hot = wsp.hot
        if wsp.hot_flow:
            self.hot_flow = wsp.hot_flow

        wspService = WspService()
        self.next_review_date = wspService.NextReviewDate(wsp=wsp)
        self.alert_level = wspService.AlertLevel(wsp=wsp)
        # actions da fare
