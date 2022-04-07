from datetime import date

from views import Index, Products, Contacts, CreateCategory, CreateProduct, ProductsList


def copyright_year(request):
    """Получает значение текущего года и передает в шаблон"""
    request['year'] = date.today().year


fronts = [copyright_year]

routes = {
    '/': Index(),
    '/products/': Products(),
    '/contacts/': Contacts(),
    '/products/create-category/': CreateCategory(),
    '/products/create-product/': CreateProduct(),
    '/products/category/': ProductsList()
}
