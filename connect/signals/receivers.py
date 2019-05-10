from django.db.models.signals import pre_delete
from django.dispatch import receiver

from connect.models import DeviceRegistration


@receiver(pre_delete, sender=DeviceRegistration)
def deleting_device_registration(instance: DeviceRegistration, **_kwargs):
    instance.delete_from_hive_manager()
