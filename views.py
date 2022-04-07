"""Описание представлений"""
from framework.templator import render
from patterns.pattern_creator import Engine, Logger

ENGINE = Engine()
LOGGER = Logger('main')


class Index:
    """Представление главной страницы"""

    def __call__(self, request):
        title = 'Главная'

        context = {
            'title': title,
            'year': request.get('year'),
            'path': request.get('path'),
            'product_list': ENGINE.get_main_products()
        }

        LOGGER.log(f'Сформирована главная страница с контекстом: {context}')

        return '200 OK', render('index.html', context=context)


class Products:
    """Представление страницы с продуктами"""

    def __call__(self, request):
        title = 'Продукты'

        context = {
            'title': title,
            'year': request.get('year'),
            'path': request.get('path'),
            'product_list': ENGINE.get_all_products(),
            'category_list': ENGINE.get_all_categories()
        }

        return '200 OK', render('products.html', context=context)


class CreateCategory:
    """Представление страницы создания категории"""

    def __call__(self, request):
        title = 'Создание категории'

        context = {
            'title': title,
            'year': request.get('year'),
            'path': request.get('path'),
            'product_list': ENGINE.get_all_products(),
            'category_list': ENGINE.get_all_categories()
        }

        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = ENGINE.decode_value(name)
            category_id = data.get('category_id')
            category = None

            if category_id.isdigit():
                category = ENGINE.get_category_by_id(int(category_id))

            new_category = ENGINE.create_category(name, category)

            ENGINE.categories.append(new_category)

            LOGGER.log(f'Создана категория {name}')

            return '302 Found', [('Location', '/')]
        else:
            return '200 OK', render('create_category.html', context=context)


class CreateProduct:
    """Представление страницы создания продукта"""
    category_id = - 1

    def __call__(self, request):
        title = 'Создание категории'

        context = {
            'title': title,
            'year': request.get('year'),
            'path': request.get('path'),
            'category_list': ENGINE.get_all_categories(),
            'error': ''
        }

        if request['method'] == 'POST':
            data = request['data']

            category_id = data['category_id']
            if not category_id.isdigit():
                context['error'] = 'Необходимо выбрать категорию'
                return '200 OK', render('create_product.html', context=context)
            product_type = data['product_type']
            name = data['name']
            price = data['price']

            category = ENGINE.get_category_by_id(int(category_id))
            product = ENGINE.create_product(product_type, name, category, price)
            ENGINE.products.append(product)

            LOGGER.log(f'Создан продукт {name}')

            return '302 Found', [('Location', f'/products/category/?id={category_id}')]
        else:
            return '200 OK', render('create_product.html', context=context)


class ProductsList:
    """Представление страницы товаров для категории"""
    category_id = -1

    def __call__(self, request):
        self.category_id = request['request_params']['id']
        if self.category_id != -1:
            products_list = ENGINE.get_products_by_category(int(self.category_id))
        else:
            products_list = []

        title = f'Продукты'

        context = {
            'title': title,
            'year': request.get('year'),
            'path': request.get('path'),
            'product_list': products_list,
            'category_list': ENGINE.get_all_categories()
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
