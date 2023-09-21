from bboard.models import Rubric


def my_middleware(next):
    # Здесь можно выполнить какую-либо инициализацию
    def core_middleware(request):
        # Здесь выполняется обработка клиентского запроса
        response = next(request)
        # Здесь выполняется обработка ответа
        return response

    return core_middleware


class MyMiddleware:
    def __int__(self, next):
        self._next = next
        # Здесь можно выполнить какую-либо инициализацию

    def __call__(self, request):
        # Здесь выполняется обработка клиентского запроса
        response = self._next(request)
        # обработка ответа
        return response


class RubricMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        return self._get_response(request)

    def process_template_response(self, request, response):
        response.context_data['rubrics'] = Rubric.objects.all()
        return response
