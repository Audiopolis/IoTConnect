from django.apps import AppConfig


class ConnectConfig(AppConfig):
    name = 'connect'

    def ready(self):
        from connect.signals.receivers import deleting_device_registration  # noqa
