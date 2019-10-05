from django.http import JsonResponse


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
