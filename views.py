"""Описание представлений"""
from datetime import date

import variables
from framework.templator import render
from patterns.pattern_creator import Engine, Logger, AppRoute, AppTime, ProductsSerializer, CreateView, ListView, \
    EmailOrderNotifier, SmsOrderNotifier, PayPalPayment, CardPayment

ENGINE = Engine()
LOGGER = Logger('main', 'file')
EMAIL_NOTIFIER = EmailOrderNotifier()
SMS_NOTIFIER = SmsOrderNotifier()

routes = {}


@AppRoute(routes=routes, url='/')
class Index:
    """Представление главной страницы"""

    @AppTime('Index')
    def __call__(self, request):
        title = 'Главная'

        context = {
            'title': title,
            'year': request.get('year'),
            'path': request.get('path'),
            'user': request.get('user'),
            'product_list': ENGINE.get_main_products()
        }

        LOGGER.log(f'Сформирована главная страница с контекстом: {context}')

        return '200 OK', render('index.html', context=context)


@AppRoute(routes=routes, url='/products/')
class Products:
    """Представление страницы с продуктами"""

    @AppTime('Products')
    def __call__(self, request):
        title = 'Продукты'

        context = {
            'title': title,
            'year': request.get('year'),
            'path': request.get('path'),
            'user': request.get('user'),
            'product_list': ENGINE.get_all_products(),
            'category_list': ENGINE.get_all_categories()
        }

        return '200 OK', render('products.html', context=context)


@AppRoute(routes=routes, url='/products/create-category/')
class CreateCategory:
    """Представление страницы создания категории"""

    @AppTime('Create_category')
    def __call__(self, request):
        title = 'Создание категории'

        context = {
            'title': title,
            'year': request.get('year'),
            'path': request.get('path'),
            'user': request.get('user'),
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


@AppRoute(routes=routes, url='/products/create-product/')
class CreateProduct:
    """Представление страницы создания продукта"""
    category_id = - 1

    @AppTime('Create_product')
    def __call__(self, request):
        title = 'Создание категории'

        context = {
            'title': title,
            'year': request.get('year'),
            'path': request.get('path'),
            'user': request.get('user'),
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


@AppRoute(routes=routes, url='/products/category/')
class ProductsList:
    """Представление страницы товаров для категории"""
    category_id = -1

    @AppTime('Products_list')
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
            'user': request.get('user'),
            'product_list': products_list,
            'category_list': ENGINE.get_all_categories()
        }

        return '200 OK', render('products.html', context=context)


@AppRoute(routes=routes, url='/contacts/')
class Contacts:
    """Представление страницы контактов"""

    @AppTime('Contacts')
    def __call__(self, request):
        title = 'Контакты'

        context = {
            'title': title,
            'path': request.get('path'),
            'year': request.get('year'),
            'user': request.get('user')
        }

        return '200 OK', render('contact.html', context=context)


@AppRoute(routes=routes, url='/products/load/')
class LoadData(CreateView):
    """Заполняет базу из файла json"""
    template_name = 'fill_db.html'
    redirect_url = '/products/'

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Загрузка данных'
        context['year'] = date.today().year

        return context

    def create_obj(self, data: dict):
        if data['data_category']:
            with open('json/category.json', 'r', encoding='utf-8') as f:
                load_data = ProductsSerializer([]).load(f.read())
            if load_data:
                for item in load_data:
                    new_category = ENGINE.create_category(item['name'])
                    ENGINE.categories.append(new_category)
                    LOGGER.log(f"Создана категория {item['name']}")
        if data['data_product']:
            with open('json/products.json', 'r', encoding='utf-8') as f:
                load_data = ProductsSerializer([]).load(f.read())
            if load_data:
                for item in load_data:
                    category = ENGINE.get_category_by_name(item['category'])
                    name = item['name']
                    price = item['price']
                    product_type = item['product_type']

                    new_product = ENGINE.create_product(product_type, name, category, price)
                    ENGINE.products.append(new_product)

                    LOGGER.log(f"Создан продукт {name}")


@AppRoute(routes=routes, url='/create_user/')
class CreateUser(CreateView):
    """Создание пользователя"""
    template_name = 'create_user.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Создание пользователя'
        context['year'] = self.request.get('year')
        context['path'] = self.request.get('path')

        return context

    def create_obj(self, data: dict):
        user_type = data['user_type']
        name = data['name']
        password = data['password']
        user = ENGINE.create_user(user_type, name, password)
        if user_type == 'buyer':
            ENGINE.buyers.append(user)
        else:
            ENGINE.staff.append(user)

        LOGGER.log(f'Создан пользователь {name}')


@AppRoute(routes=routes, url='/product/buy/')
class BuyProduct:
    """Добавление товара в корзину и создание корзины, если ее нет"""
    product_id = -1
    path = '/'

    def __call__(self, request):
        self.product_id = request['request_params']['id']
        self.path = request['request_params']['path']
        self.user = request.get('user')

        if self.product_id != -1:
            if self.user == 'Анонимный':
                return '302 Found', [('Location', f'/login/')]
            basket = ENGINE.create_basket(self.user)
            product = ENGINE.get_product_by_id(int(self.product_id))
            basket.add_to_basket(product)
            return '302 Found', [('Location', f'{self.path}')]


@AppRoute(routes=routes, url='/login/')
class Login(CreateView):
    """Авторизация пользователя"""
    template_name = 'login.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Вход'
        context['year'] = self.request.get('year')
        context['path'] = self.request.get('path')

        return context

    def create_obj(self, data):
        name = data['name']
        password = data['password']
        try:
            user = ENGINE.get_user_by_name(name)
        except Exception as err:
            print(err)
        else:
            if user.password == password:
                user.login()
            else:
                print('Ошибка авторизации. Не верный пароль')


@AppRoute(routes=routes, url='/logout/')
class Logout:
    """Выход пользователя"""
    path = '/'

    def __call__(self, request):
        name = request.get('user')
        try:
            user = ENGINE.get_user_by_name(name)
        except Exception as err:
            print(err)
        else:
            user.logout()

        return '302 Found', [('Location', f'{self.path}')]


@AppRoute(routes=routes, url='/basket/')
class BasketList(ListView):
    """Отображение корзины"""
    # basket = ENGINE.get_basket(variables.AUTH_USER)
    try:
        queryset = ENGINE.get_basket(variables.AUTH_USER).get_product_list()
    except Exception as err:
        print(err)
    template_name = 'basket.html'


@AppRoute(routes=routes, url='/create_order/')
class Order:
    """Создание заказа"""
    def __call__(self, request):
        user = request['request_params']['user']
        basket = ENGINE.get_basket(user)
        if not basket:
            return '302 Found', [('Location', f'/')]
        order = ENGINE.create_order(basket)
        order.attach(EMAIL_NOTIFIER)
        order.attach(SMS_NOTIFIER)
        ENGINE.orders.append(order)

        title = 'Заказ'

        context = {
            'title': title,
            'year': request.get('year'),
            'user': user,
            'total': order.get_total_price(),
            'order': order
        }

        if request['method'] == 'POST':
            data = request['data']
            pay_method = data['pay_method']

            if pay_method == 'paypal':
                pay_method = PayPalPayment('example@mail.ru', 'example_token')
            elif pay_method == 'card':
                pay_method = CardPayment('1234-1234-1234-1234')

            order.pay(pay_method)

            return '302 Found', [('Location', '/')]
        else:
            return '200 OK', render('order.html', context=context)
