from django.contrib import admin

from connect.models import FeideIdentity, DeviceRegistration


@admin.register(FeideIdentity)
class FeideIdentityAdmin(admin.ModelAdmin):
    list_display = ['feide_user_id', 'name']
    search_fields = ['feide_user_id', 'name']

    @staticmethod
    def disable_all_devices(_instance, _request, queryset):
        for feide_identity in queryset:
            for device_registration in feide_identity.device_registrations.all():
                if device_registration.enabled:
                    device_registration.enabled = False
                    device_registration.save()

    actions = ('disable_all_devices',)


@admin.register(DeviceRegistration)
class DeviceRegistrationAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'feide_id', 'get_name', 'get_feide_user_id', 'device_description',
                    'enabled']
    list_select_related = True
    list_filter = ['enabled']
    search_fields = ['feide_id', 'feide_id__name', 'feide_id__feide_user_id']

    @staticmethod
    def disable(_instance, _request, queryset):
        for device_registration in queryset:
            if device_registration.enabled:
                device_registration.enabled = False
                device_registration.save()

    actions = ('disable',)

    @staticmethod
    def get_name(obj):
        return obj.feide_id.name

    @staticmethod
    def get_feide_user_id(obj):
        return obj.feide_id.feide_user_id
