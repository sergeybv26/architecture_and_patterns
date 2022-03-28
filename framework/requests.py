"""Содержит классы-обработчики GET и POST запросов"""


class GetRequest:
    """Выполняет обработку GET запроса"""
    @staticmethod
    def parse_input_data(data: str):
        """
        Осуществляет парсинг строки с параметрами и создает словарь с параметрами
        :param data: строка с параметрами
        :return:словарь
        """
        result = {}

        if data:
            params = data.split('&')
            for item in params:
                key, value = item.split('=')
                result[key] = value

        return result

    @staticmethod
    def get_request_params(environ):
        """
        Получает строку с параметрами из запроса, возвращает словарь с параметрами
        :param environ: переменные окружения
        :return:словарь
        """
        query_str = environ['QUERY_STRING']

        request_params = GetRequest.parse_input_data(query_str)

        return request_params


class PostRequest:
    """Выполняет обработку POST запроса"""

    @staticmethod
    def parse_input_data(data: str):
        """
        Осуществляет парсинг строки с параметрами и создает словарь с параметрами
        :param data: строка с параметрами
        :return:словарь
        """
        result = {}

        if data:
            params = data.split('&')
            for item in params:
                key, value = item.split('=')
                result[key] = value

        return result

    @staticmethod
    def get_input_data(environ):
        """
        Осуществляет проверку наличия и считывание данных запроса
        :param environ:переменные окружения
        :return:байты данных
        """
        content_length_str = environ.get('CONTENT_LENGTH')

        if content_length_str:
            content_length = int(content_length_str)
        else:
            content_length = 0

        data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''

        return data

    def parse_wsgi_data(self, data: bytes):
        """
        Осуществляет декодирование и парсинг данных запроса и возвращает словарь с параметрами
        :param data: данные запроса в байтах
        :return: словарь с параметрами запроса
        """

        if data:
            data_str = data.decode(encoding='utf-8')
        else:
            data_str = ''

        return self.parse_input_data(data_str)

    def get_request_params(self, environ):
        """
        Осуществляет получение запроса и преобразование его в словарь
        :param environ:переменные окружения
        :return:словарь с параметрами запроса
        """
        data_bytes = self.get_input_data(environ)
        data = self.parse_wsgi_data(data_bytes)

        return data
