"""Главный модуль фреймворка"""
from quopri import decodestring

from framework.requests import PostRequest, GetRequest


class PageNotFound404:
    """Класс-описывает обработку запроса к несуществующей странице"""

    def __call__(self, request):
        return '404 WHAT', 'Page not found'


class FrameworkApp:
    """Класс-основа фреймворка"""

    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = path + '/'

        request = {}
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequest().get_request_params(environ)
            request['data'] = self.decode_value(data)
            print(f"Получен POST-запрос: {request['data']}")
        elif method == "GET":
            request_params = GetRequest().get_request_params(environ)
            request['request_params'] = self.decode_value(request_params)
            print(f"Получен GET-запрос: {request['request_params']}")

        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound404()

        for front in self.fronts:
            front(request)

        code, body = view(request)

        start_response(code, [('Content-Type', 'text/html')])

        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data: dict):
        """
        Осуществляет декодирование кириллицы и специальных символов
        :param data: словарь с кодированными значениями
        :return: словарь с декодированными значениями
        """
        decode_data = {}
        for key, value in data.items():
            value_bytes = bytes(value.replace('%', '=').replace('+', ' '), 'UTF-8')
            value_decode_str = decodestring(value_bytes).decode('UTF-8')
            decode_data[key] = value_decode_str

        return decode_data
