"""Описание представлений"""
from framework.templator import render

# Так как работаем без базы данных, создадим список с параметрами товаров
PRODUCTS = [
    {
        'name': 'Полка для обуви, металл, дерево, 3 секции, 76х31х49 см, с сиденьем, орех, бежевая, Sheffilton',
        'category': 'Хранение',
        'price': 4726,
        'desc': 'Полка-банкетка является отличным решением для домашнего интерьера',
        'img': '/static/img/1.jpeg'
    },
    {
        'name': 'Вешалка напольная Sheffilton M-3026 В1-60, венге/черный',
        'category': 'Хранение',
        'price': 6958,
        'desc': 'Функциональная компакт-прихожая',
        'img': '/static/img/2.jpg'
    },
    {
        'name': 'Качели садовые Кокон, 150 кг, Green Days, серые, ротанг, подушка малиновая',
        'category': 'Сад',
        'price': 26991,
        'desc': 'Подвесное кресло Кокон Green Days идет в комплекте со стойкой',
        'img': '/static/img/3.jpg'
    },
    {
        'name': 'Постельное белье евростандарт, простыня 220х240 см, 2 наволочки 50х70 см, пододеяльник 200х220 см',
        'category': 'Текстиль',
        'price': 3509,
        'desc': 'Постельное белье из поплина обладает хорошей воздухопроницаемостью и при этом прекрасно держит тепло. '
                'Белье мягкое, легко гладится и обладает прекрасными органолептическими свойствами',
        'img': '/static/img/4.jpg'
    },
    {
        'name': 'Плед 1.5-спальный, 150х180 см',
        'category': 'Текстиль',
        'price': 2290,
        'desc': 'Плед произведён из натурального хлопка и бамбука',
        'img': '/static/img/5.jpg'
    },
]


def get_main_product():
    """
    Получает популярные товары
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
            'path': request.get('path'),
            'product_list': get_main_product()
        }

        return '200 OK', render('index.html', context=context)


class Products:
    """Представление страницы с продуктами"""
    def __call__(self, request):
        title = 'Продукты'

        context = {
            'title': title,
            'year': request.get('year'),
            'path': request.get('path'),
            'product_list': PRODUCTS
        }

        return '200 OK', render('products.html', context=context)


class Contacts:
    """Представление страницы контактов"""
    def __call__(self, request):
        title = 'Контакты'

        context = {
            'title': title,
            'path': request.get('path'),
            'year': request.get('year')
        }

        return '200 OK', render('contact.html', context=context)
