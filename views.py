"""Описание представлений"""
from framework.templator import render


class Index:
    """Представление главной страницы"""
    def __call__(self, request):
        title = 'Главная'

        context = {
            title: title,
        }

        return '200 OK', render('index.html', context)
