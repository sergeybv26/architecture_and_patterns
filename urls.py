from datetime import date


def copyright_year(request):
    """Получает значение текущего года и передает в шаблон"""
    request['year'] = date.today().year


fronts = [copyright_year]
