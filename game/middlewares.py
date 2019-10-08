import json

from django.http import JsonResponse, QueryDict, HttpResponse


def is_logged_in(get_response):
    def middleware(request):
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 'error',
                'message': 'not authenticated'
            })
        response = get_response(request)

        return response

    return middleware


class JSONMiddleware:
    """
    Process application/json requests data from GET and POST requests.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.META.get('CONTENT_TYPE') and 'application/json' in request.META.get('CONTENT_TYPE'):
            try:
                data = json.loads(request.body)
                q_data = QueryDict('', mutable=True)
                for key, value in data.items():
                    if isinstance(value, list):
                        for x in value:
                            q_data.update({key: x})
                    else:
                        q_data.update({key: value})

                if request.method == 'GET':
                    request.GET = q_data

                if request.method == 'POST':
                    request.POST = q_data

                return self.get_response(request)
            except Exception as e:
                return HttpResponse("JSON Decode Error", status=400)

        return self.get_response(request)
