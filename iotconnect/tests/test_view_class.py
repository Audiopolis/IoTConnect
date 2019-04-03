from rest_framework.test import APITestCase


class IotConnectViewTest(APITestCase):
    def test_class__view_set_up_without_adapter__bad_request(self):
        pass

    def test_class__view_set_up_without_authenticator_and_authentication_is_required__bad_request(self):
        pass

    def test_class__view_set_up_without_authenticator_and_authentication_is_not_required__bad_request(self):
        pass

    def test_class__view_set_up_correctly_but_no_logic_in_adapter_or_authenticator__ok(self):
        pass
