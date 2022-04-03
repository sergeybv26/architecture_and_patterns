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
        return UserFactory.create(user_type, name, password)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def get_category_by_id(self, _id):
        for category in self.categories:
            if category.id == _id:
                return category
        raise Exception(f'Не найдена категория с id = {_id}')

    def get_category_by_name(self, name):
        for category in self.categories:
            if category.name == name:
                return category
        raise Exception(f'Категория {name} не найдена')


