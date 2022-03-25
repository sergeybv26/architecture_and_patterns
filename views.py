"""Описание представлений"""
from framework.templator import render

# Так как работаем без базы данных, создадим список с параметрами товаров
PRODUCTS = [
    {
        'name': '',
        'price': 1000,
        'desc': '',
        'img': '/static/img/1.jpg'
    },
{
        'name': '',
        'price': 1000,
        'desc': '',
        'img': '/static/img/1.jpg'
    },
{
        'name': '',
        'price': 1000,
        'desc': '',
        'img': '/static/img/1.jpg'
    },
{
        'name': '',
        'price': 1000,
        'desc': '',
        'img': '/static/img/1.jpg'
    },
{
        'name': '',
        'price': 1000,
        'desc': '',
        'img': '/static/img/1.jpg'
    },
]


def get_main_product():
    """
    Получает горячие товары
    :return: Список словарей
    """
    return PRODUCTS[-3:]


class Index:
    """Представление главной страницы"""

    def __call__(self, request):
        title = 'Главная'

        context = {
            'title': title,
            'year': request.get('year'),
            'product_list': get_main_product()
        }

        return '200 OK', render('index.html', context=context)
