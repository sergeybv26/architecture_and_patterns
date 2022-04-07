from wsgiref.simple_server import make_server


from framework.main import FrameworkApp
from urls import fronts
from views import routes

if __name__ == '__main__':
    application = FrameworkApp(routes, fronts)
    port = 8081
    with make_server('', port, application) as httpd:
        print(f'Запущен сервер на порту {port}...')
        httpd.serve_forever()
