from datetime import date

import variables


def copyright_year(request):
    """Получает значение текущего года и передает в шаблон"""
    request['year'] = date.today().year


def auth_user(request):
    """Получает имя зарегистрированного пользователя"""
    request['user'] = variables.AUTH_USER


fronts = [copyright_year, auth_user]
