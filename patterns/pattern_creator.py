from quopri import decodestring
from time import time


class AbstractUser:
    """Класс абстрактного пользователя"""
    def __init__(self, name, password):
        self.name = name
        self.password = password


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


class Engine:
    """Основной класс"""
    def __init__(self):
        self.buyers = []
        self.staff = []
        self.products = []
        self.categories = []

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
    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)


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
