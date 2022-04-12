from abc import ABCMeta, abstractmethod
from quopri import decodestring
from time import time

from jsonpickle import dumps, loads

from framework.templator import render


class AbstractUser:
    """Класс абстрактного пользователя"""
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.is_login = False

    def login(self):
        self.is_login = True

    def logout(self):
        self.is_login = False


class Buyer(AbstractUser):
    """Класс покупателя"""
    pass


class Staff(AbstractUser):
    """Класс персонала"""
    pass


class UserFactory:
    """Фабрика пользователей"""
    user_types = {
        'buyer': Buyer,
        'staff': Staff
    }

    @classmethod
    def create(cls, user_type, name, password):
        return cls.user_types[user_type](name, password)


class Product:
    """Класс абстрактного продукта"""
    id_count = 0

    def __init__(self, name, category, price):
        self.id = Product.id_count
        Product.id_count += 1
        self.name = name
        self.category = category
        self.price = price
        self.category.products.append(self)
        self.desc = ''
        self.img = ''


class RealProduct(Product):
    """Класс товара"""
    pass


class ServiceProduct(Product):
    """Класс услуги"""
    pass


class ProductFactory:
    """Фабрика продуктов"""
    product_types = {
        'product': RealProduct,
        'service': ServiceProduct
    }

    @classmethod
    def create(cls, product_type, name, category, price):
        return cls.product_types[product_type](name, category, price)


class Category:
    """Класс категории"""
    id_count = 0

    def __init__(self, name, category):
        self.id = Category.id_count
        Category.id_count += 1
        self.name = name
        self.category = category
        self.products = []
        self.desc = ''
        self.img = ''


class Basket:
    """Класс корзины"""
    def __init__(self, user):
        self.user = user
        self.product_list = []

    def add_to_basket(self, product):
        self.product_list.append(product)

    def remove_from_basket(self, product):
        self.product_list.remove(product)

    def get_product_list(self):
        return self.product_list

    def get_user(self):
        return self.user


class Order:
    """Класс заказа"""
    def __init__(self, basket):
        self.user = basket.get_user()
        self.product_list = basket.get_product_list()

    def get_total_price(self):
        total_price = 0
        for item in self.product_list:
            total_price += item.price

        return total_price

    def pay(self, pay_method):
        total = self.get_total_price()
        pay_method.pay(total)


class Engine:
    """Основной класс"""
    def __init__(self):
        self.buyers = []
        self.staff = []
        self.products = []
        self.categories = []
        self.baskets = []

    @staticmethod
    def create_user(user_type, name, password):
        """
        Создает пользователя
        :param user_type: тип пользователя (покупатель или сотрудник)
        :param name: имя пользователя
        :param password: пароль
        :return: экземпляр класса пользователя соответствующего типа
        """
        return UserFactory.create(user_type, name, password)

    @staticmethod
    def create_category(name, category=None):
        """
        Создает категорию
        :param name: имя категории
        :param category: имя родительской категории, если создаем подкатегорию
        :return: экземпляр класса категории
        """
        return Category(name, category)

    def get_category_by_id(self, _id):
        """
        Осуществляет поиск категории по id
        :param _id: id искомой категории
        :return: экземпляр класса категории
        """
        for category in self.categories:
            if category.id == _id:
                return category
        raise Exception(f'Не найдена категория с id = {_id}')

    def get_category_by_name(self, name):
        """
        Осуществляет поиск категории по имени
        :param name: имя категории
        :return: экземпляр класса категории
        """
        for category in self.categories:
            if category.name == name:
                return category
        raise Exception(f'Категория {name} не найдена')

    def get_all_categories(self):
        """Получает список всех категорий"""
        return self.categories

    @staticmethod
    def create_product(product_type, name, category, price):
        """
        Создает товар
        :param product_type: Тип товара (продукт или услуга)
        :param name: наименование товара
        :param category: категория товара
        :param price: цена товара
        :return: экземпляр соответствующего класса товара
        """
        return ProductFactory.create(product_type, name, category, price)

    def get_product_by_id(self, _id):
        """
        Выполняет поиск товара по id
        :param _id: id товара
        :return: экземпляр класса товара
        """
        for product in self.products:
            if product.id == _id:
                return product
        raise Exception(f'Не найден продукт с id = {_id}')

    def get_product_by_name(self, name):
        """
        Выполняет поиск товара по имени
        :param name: имя товара
        :return: экземпляр класса товара
        """
        for product in self.products:
            if product.name == name:
                return product
        raise Exception(f'Продукт {name} не найден')

    def get_all_products(self):
        """Получает список всех товаров"""
        return self.products

    def get_main_products(self):
        """Получает список популярных товаров"""
        main_products = []
        try:
            main_products = self.products[-3:]
        except IndexError:
            print('Отсутствуют товары в базе')
        return main_products

    def get_products_by_category(self, category_id):
        """Получает список продуктов категории"""
        for category in self.categories:
            if category.id == category_id:
                return category.products
        return []

    def create_basket(self, user):
        """
        Создает корзину пользователя
        :param user: пользователь
        :return: экземпляр класса корзины пользователя
        """
        for basket in self.baskets:
            if basket.user == user:
                return basket
        return Basket(user)

    def get_basket(self, user):
        """Получает корзину пользователя"""
        for basket in self.baskets:
            if basket.user == user:
                return basket
        return None

    @staticmethod
    def decode_value(val):
        """
        Осуществляет декодирование кириллицы и специальных символов
        :param val: декодируемое значение
        :return: декодированное значение
        """
        value_bytes = bytes(val.replace('%', '=').replace('+', ' '), 'UTF-8')
        value_decode_str = decodestring(value_bytes).decode('UTF-8')

        return value_decode_str


class SingletonByName(type):
    """Метакласс синглтон по имени"""
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        elif kwargs:
            name = kwargs['name']
        else:
            name = None

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):
    """Класс логгера"""
    def __init__(self, name, writer_type='file'):
        self.name = name
        self.writer = WriterFabric().get_writer(writer_type)

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)


class AppRoute:
    """Паттерн-декоратор, создающий маршруты для представлений"""
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


class AppTime:
    """паттерн-декоратор, осуществляет подсчет и вывод времени работы методов декорируемого класса"""
    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def timeit(method):
            def timed(*args, **kwargs):
                start_time = time()
                result = method(*args, **kwargs)
                end_time = time()
                time_delta = end_time - start_time
                print(f'debug -->> {self.name} выполнялся {time_delta:2.2f} мс')
                return result
            return timed
        return timeit(cls)


class ProductsSerializer:
    """класс паттерн-хранитель, осуществляющий сериализацию базы товаров"""
    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return dumps(self.obj)

    @staticmethod
    def load(data):
        return loads(data)


class TemplateView:
    """Поведенческий паттерн. Шаблонный метод"""
    template_name = 'template.html'
    redirect_url = '/'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def get_redirect_url(self):
        return self.redirect_url

    def render_template(self):
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', render(template_name, context)

    def success_redirect(self):
        url = self.get_redirect_url()
        return '302 Found', [('Location', url)]

    def __call__(self, request):
        return self.render_template()


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_obj(data)

            return self.success_redirect()
        else:
            return super().__call__(request)


class ConsoleWriter:
    def write(self, text):
        print(text)


class FileWriter:
    def __init__(self, filename='log.txt'):
        self.filename = filename

    def write(self, text):
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')


class WriterFabric:
    @staticmethod
    def get_writer(writer_type):
        if writer_type == 'file':
            return FileWriter()
        elif writer_type == 'console':
            return ConsoleWriter()


class Payment(metaclass=ABCMeta):
    """Абстрактный класс. Паттерн-стратегия процесса оплаты"""
    @abstractmethod
    def pay(self, amount):
        pass


class PayPalPayment(Payment):
    def __init__(self, email, token):
        self.email = email
        self.token = token

    def pay(self, amount):
        print(f'Выполнена оплата на сумму {amount} через PayPal аккаунт {self.email}')


class CardPayment(Payment):
    def __init__(self, card_num):
        self.card = card_num

    def pay(self, amount):
        print(f'Выполнена оплата на сумму {amount} с карты № {self.card}')
