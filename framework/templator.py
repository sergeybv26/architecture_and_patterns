import os.path

from jinja2 import Template


def render(template_name, folder='templates', **kwargs):
    """
    Осуществляет рендер шаблона с полученными параметрами
    :param template_name: имя файла-шаблона
    :param folder: папка, в которой расположен шаблон
    :param kwargs: именованные параметры
    :return: рендер шаблона с параметрами
    """
    file_path = os.path.join(folder, template_name)
    with open(file_path, encoding='utf-8') as f:
        template = Template(f.read())

    return template.render(**kwargs)
