from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, context, folder='templates'):
    """
    Осуществляет рендер шаблона с полученными параметрами
    :param template_name: имя файла-шаблона
    :param folder: папка, в которой расположен шаблон
    :param context: именованные параметры
    :return: рендер шаблона с параметрами
    """
    env = Environment()
    env.loader = FileSystemLoader(folder)

    template = env.get_template(template_name)

    return template.render(**context)
