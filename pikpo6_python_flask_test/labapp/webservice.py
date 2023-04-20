from typing import List

from config import DB_URL                       # параметры подключения к БД из модуля конфигурации config.py
from .repository import sql_api                 # подключаем API для работы с БД
from .repository.connectorfactory import SQLStoreConnectorFactory

"""
    В данном модуле реализуются бизнес-логика обработки клиентских запросов.
    Здесь также могут применяться SQL-методы, представленные в модуле repository.sql_api
"""

# Структура основного навигационнго меню (<nav>) веб-приложения,
# оформленное в виде объекта dict
navmenu = [
    {
        'name': 'HOME',
        'addr': '/'
    },
    {
        'name': 'ABOUT',
        'addr': '#'
    },
    {
        'name': 'CONTACT US',
        'addr': '/contact'
    },
]


def get_source_files_list() -> List[tuple]:
    """ Получаем список обработанных файлов """
    db_connector = SQLStoreConnectorFactory().get_connector(DB_URL)  # инициализируем соединение
    db_connector.start_transaction()  # начинаем выполнение запросов (открываем транзакцию)
    result = sql_api.select_all_from_source_files(db_connector)  # получаем список всех обработанных файлов
    db_connector.end_transaction()  # завершаем выполнение запросов (закрываем транзакцию)
    db_connector.close()
    return result


def get_processed_data(source_file: int) -> List[tuple]:
    """ Получаем обработанные данные из основной таблицы """
    db_connector = SQLStoreConnectorFactory().get_connector(DB_URL)
    db_connector.start_transaction()  # начинаем выполнение запросов (открываем транзакцию)
    result = sql_api.select_rows_from_processed_data(db_connector, source_file=source_file)
    db_connector.end_transaction()  # завершаем выполнение запросов (закрываем транзакцию)
    db_connector.close()
    return result

def get_files(form) -> List[tuple]:
    """ Получаем обработанные данные с фильтрами """
    db_connector = SQLStoreConnectorFactory().get_connector(DB_URL)
    db_connector.start_transaction()  # начинаем выполнение запросов (открываем транзакцию)
    result = sql_api.select_processed_data(db_connector, form)
    db_connector.end_transaction()  # завершаем выполнение запросов (закрываем транзакцию)
    db_connector.close()
    return result


def post_msg(form) -> List[tuple]:
    """ Получаем обработанные данные с фильтрами """
    db_connector = SQLStoreConnectorFactory().get_connector(DB_URL)
    db_connector.start_transaction()  # начинаем выполнение запросов (открываем транзакцию)
    result = sql_api.addUser(db_connector, form)
    db_connector.end_transaction()  # завершаем выполнение запросов (закрываем транзакцию)
    db_connector.close()
    return result

def get_data_user(login: str)-> List[tuple]:
    db_connector = SQLStoreConnectorFactory().get_connector(DB_URL)
    db_connector.start_transaction()  # начинаем выполнение запросов (открываем транзакцию)
    result = sql_api.get_user(db_connector, login)
    db_connector.end_transaction()  # завершаем выполнение запросов (закрываем транзакцию)
    db_connector.close()
    return result

def get_data_psw_log(psw: str, login: str)-> List[tuple]:
    db_connector = SQLStoreConnectorFactory().get_connector(DB_URL)
    db_connector.start_transaction()  # начинаем выполнение запросов (открываем транзакцию)
    result = sql_api.get_pass_log(db_connector, psw, login)
    db_connector.end_transaction()  # завершаем выполнение запросов (закрываем транзакцию)
    db_connector.close()
    return result

def get_data_id(id: str)-> List[tuple]:
    db_connector = SQLStoreConnectorFactory().get_connector(DB_URL)
    db_connector.start_transaction()  # начинаем выполнение запросов (открываем транзакцию)
    result = sql_api.get_id(db_connector, id)
    db_connector.end_transaction()  # завершаем выполнение запросов (закрываем транзакцию)
    db_connector.close()
    return result
