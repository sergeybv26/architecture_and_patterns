"""Обработчик ошибок"""


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Запись не найдена: {message}')


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Ошибка записи в БД: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Ошибка обновления данных: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Ошибка удаления данных: {message}')
