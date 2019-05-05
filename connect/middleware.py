from django.http import HttpResponse

from connect.exceptions import NoDataportenCodeError


class CustomExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, _request, exception):
        if isinstance(exception, NoDataportenCodeError):
            return HttpResponse("The service is currently unavailable", status=503)
