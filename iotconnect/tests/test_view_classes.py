from django.http import HttpRequest
from rest_framework.test import APITestCase

from iotconnect.classes import IotConnectView, Authenticator, AdHocAdapter


class IotConnectViewTest(APITestCase):
    def setUp(self):
        self.view = IotConnectView()

    def test_class__view_set_up_without_adapter__attribute_error(self):
        self.view.authenticator = Authenticator()
        try:
            self.view.dispatch(request=HttpRequest())
            self.fail("ad_hoc_adapter should be required")
        except AttributeError as ex:
            self.assertEqual('ad_hoc_adapter must be set', ex.args[0])

    def test_class__view_set_up_without_authenticator_and_authentication_is_required__attribute_error(self):
        self.view.ad_hoc_adapter = AdHocAdapter()
        self.view.requires_authentication = True
        try:
            self.view.dispatch(request=HttpRequest())
            self.fail("authenticator should be required if requires_authentication is True")
        except AttributeError as ex:
            self.assertEqual('authenticator must be set if requires_authentication is True', ex.args[0])

    def test_class__view_set_up_without_authenticator_and_authentication_is_not_required__not_attribute_error(self):
        self.view.ad_hoc_adapter = AdHocAdapter()
        self.view.requires_authentication = False
        try:
            self.view.dispatch(request=HttpRequest())
        except AttributeError as ex:
            self.assertNotEqual('authenticator must be set if requires_authentication is True', ex.args[0])
