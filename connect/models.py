import json

import requests
from django.db import models
from model_utils import FieldTracker

from connect.utils import attempt_json_loads
from uninett_api.settings._secrets import OWNER_ID, HEADERS


class FeideIdentity(models.Model):
    feide_user_id = models.CharField(
        unique=True,
        verbose_name="Feide ID",
        db_index=True,
        max_length=50,
    )

    name = models.CharField(
        max_length=50,
        verbose_name="name",
        db_index=True,
        blank=True,
    )

    email = models.EmailField(
        unique=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "Feide identities"

    def __str__(self):
        return self.feide_user_id + f" ({self.name})"


class DeviceRegistration(models.Model):
    tracker = FieldTracker(fields=['enabled'])

    feide_id = models.ForeignKey(
        FeideIdentity,
        on_delete=models.CASCADE,
        related_name='device_registrations',
        verbose_name="Feide identity",
    )

    hive_manager_id = models.CharField(
        max_length=80,
        verbose_name="HiveManager identity",
    )

    device_description = models.CharField(
        max_length=100,
        verbose_name="device description",
    )

    psk = models.CharField(
        max_length=20,
        verbose_name="PSK",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="created at",
        db_index=True,
    )

    enabled = models.BooleanField(
        default=True,
        verbose_name="enabled"
    )

    def __str__(self):
        return f"{self.feide_id.__str__()}: {self.device_description}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        delete = self.tracker.has_changed('enabled') and not self.enabled
        super().save(force_insert, force_update, using, update_fields)
        if delete:
            self.delete_from_hive_manager()

    def delete_from_hive_manager(self):
        url = "https://cloud-ie.aerohive.com/xapi/v1/identity/credentials"
        get_params = {'ownerId': OWNER_ID, 'ids': [], 'userName': self.hive_manager_id}
        try:
            hive_manager_user = attempt_json_loads(requests.get(url=url, params=get_params,
                                                                headers=HEADERS)._content)['data'][0]
        except IndexError:
            return

        real_id = hive_manager_user['id']
        post_params = {'ownerId': OWNER_ID, 'ids': [real_id]}
        requests.delete(url=url, params=post_params, headers=HEADERS)
