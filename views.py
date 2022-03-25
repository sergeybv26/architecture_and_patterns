"""Описание представлений"""
from framework.templator import render


class Index:
    """Представление главной страницы"""
    def __call__(self, request):
        title = 'Главная'

        return '200 OK', render('index.html', title=title)
