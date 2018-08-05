# -*- coding: utf-8 -*-
from .models import Settings as settings_model


class SettingService(object):

    def getSettingListByDict(self, param=None, order=None):
        if not param and not order:
            return settings_model.objects.all()
        elif not order:
            return settings_model.objects.filter(
                **param
            )
        else:
            return settings_model.objects.filter(
                **param
            ).order_by(order)

    def getSettingBySettingType(self, setting_type):
        return settings_model.objects.filter(
            setting_type=setting_type
        ).order_by('position')

    def updatePosition(self, old_position, new_position, setting_type):
        # controllo se ce già una setting al posto suo
        settings_list = self.getSettingListByDict(
            param={
                'position': new_position,
                'setting_type': setting_type
            }
        )

        if settings_list:
            if new_position < old_position:
                settings_list = self.getSettingListByDict(
                    param={
                        'position__gte': new_position,
                        'setting_type': setting_type
                    },
                    order='position'
                )
                count = new_position
                for setting in settings_list:
                    setting.position += 1
                    setting.save()
                    if count == old_position:
                        break
                    count += 1

            elif new_position > old_position:
                settings_list = self.getSettingListByDict(
                    param={
                        'position__gt': old_position,
                        'setting_type': setting_type
                    },
                    order='position'
                )
                count = old_position
                for setting in settings_list:
                    setting.position -= 1
                    setting.save()
                    if count == new_position:
                        break
                    count += 1

        return new_position
