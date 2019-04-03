from django.shortcuts import redirect
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from iotconnect.utilities.enums import IotRequestMethod
from iotconnect.utilities.mixins import ValidatorMixin


class Authenticator(ValidatorMixin):
    request = None

    def is_authorized(self, validated_data) -> bool:
        raise NotImplementedError("Override is_authorized")

    def authenticate(self, authentication_data, **kwargs):
        validated_data = self.get_validated_data(authentication_data, **kwargs)
        return self.is_authorized(validated_data)


class AdHocAdapter(ValidatorMixin):
    request = None

    def perform_generation(self, validated_data) -> Response:
        raise NotImplementedError("Override perform_generation")

    def generate_psk(self, generation_options, **kwargs):
        validated_data = self.get_validated_data(generation_options, **kwargs)
        return self.perform_generation(validated_data)


class IotConnectView(APIView):
    ad_hoc_adapter: AdHocAdapter = None
    authenticator: Authenticator = None
    requires_authentication: bool = True
    authentication_data = None
    generation_options = None
    permission_classes = []
    generation_method = IotRequestMethod.POST
    authentication_failed_redirect_uri = None

    def _handler(self, request, **kwargs):
        # Ensure the presence of required data fields
        self.authentication_data, self.generation_options = self._validate_request(request)
        # Call the authenticator and return a Forbidden response if authentication fails

        if self.requires_authentication:
            # TODO: Ensure that Bad Request is returned on failure of validation
            if not self.authenticator.authenticate(self.authentication_data, **kwargs):
                if self.authentication_failed_redirect_uri is not None:
                    return redirect(to=self.authentication_failed_redirect_uri)
                return Response(status=status.HTTP_403_FORBIDDEN)
        # Generate the PSK
        response = self.ad_hoc_adapter.generate_psk(self.generation_options, **kwargs)
        return self.process(response)

    def process(self, response) -> Response:
        """
        Post processing, such as creating database entries, should be done in this method. The response should be
        returned after processing.
        :param response: The response returned by the ad hoc adapter
        """
        return response

    def dispatch(self, request, *args, **kwargs):
        """
        Overridden to validate request data and call the authentication module and PSK generator.
        """
        # Set attributes and initialize request (as done in the base method)
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers

        # Ensure that required view attributes are set
        self._validate_attributes()

        # Set the request attribute on the authenticator
        if self.authenticator:
            self.authenticator.request = request
        # Set the request attribute on the adapter (using generation_options is preferred)
        self.ad_hoc_adapter.request = request

        setattr(self, str(self.generation_method.value), self._handler)

        try:
            # Get the handler
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            # Call super's initial
            self.initial(request, *args, **kwargs)
            # Get the response
            response = handler(request, *args, **kwargs)
        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response

    def _validate_attributes(self):
        if not self.ad_hoc_adapter:
            raise AttributeError("The attribute 'ad_hoc_adapter' must be set.")
        if not self.authenticator and self.requires_authentication:
            raise AttributeError("The attribute 'authenticator' must be set if 'requires_authentication' is True.")
        if not hasattr(self.ad_hoc_adapter, 'generate_psk'):
            raise AttributeError(
                "The ad hoc adapter used should inherit the AdHocAdapter and implement all abstract methods."
            )
        if self.authenticator and not hasattr(self.authenticator, 'authenticate'):
            raise AttributeError(
                "The authenticator used should inherit the Authenticator class and implement all abstract methods."
            )

    @staticmethod
    def _validate_request(request):
        authentication_data = request.data.get('authentication_data', None)
        generation_options = request.data.get('generation_options', None)
        # Check 'is None' in case the data is empty but not null
        if authentication_data is None:
            raise ValidationError("authentication_data is required.")
        if generation_options is None:
            raise ValidationError("generation_options is required.")
        return authentication_data, generation_options
