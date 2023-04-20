from .connector import StoreConnector
import sqlite3
from .connector import StoreConnector
from flask import url_for
import math
import time
import sqlite3

class SQLiteStoreConnector(StoreConnector):
    """ Реализация коннектора для БД SQLite """
    def __init__(self, datastore):
        StoreConnector.__init__(self, datastore)
        self._cursor = None

    def connect(self):
        try:
            # Подключаемся к файлу по указанному пути без префикса 'sqlite:///'
            connection = sqlite3.connect(self._datastore[10:])
            cursor = connection.cursor()
            # Включаем поддержку внешних ключей для SQLite
            cursor.execute("PRAGMA foreign_keys = 1")
            cursor.close()
            self.connection = connection
            print("SQLite database connected.")
            return True
        except Exception as e:
            print(f'Connection error: {str(e)}')
            return False

    def execute(self, query):
        result = None
        if self._cursor is not None:
            try:
                result = self._cursor.execute(query)
            except Exception as e:
                self.connection.rollback()
                print(f'Query execution error: {str(e)}')
        else:
            print("Use start_transaction() first.")
        return result

    def start_transaction(self):
        if self._cursor is None and self.connection is not None:
            self._cursor = self.connection.cursor()

    def end_transaction(self):
        if self.connection is not None and self._cursor is not None:
            self.connection.commit()
            self._cursor.close()
            self._cursor = None

    def close(self):
        self.connection.close()
        self.connection = None

    def addUsers(self, name, login, psw):
        try:
            self.execute(f"SELECT users.id, users.name, users.login, users.psw, users.time FROM users").fetchall()
            self.execute(f"SELECT COUNT() as 'count' FROM users WHERE log LIKE '{login}'")
            self.execute(f"INSERT INTO users VALUES (NULL, ?, ?, ?)", (name, login, psw))
            self.commit()
            '''
            res = self.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким логином уже зарегистрирован")
                return False
            tm = math.floor(time.time())
            '''
            #self.execute(f"INSERT INTO users VALUES (NULL, ?, ?, ?, ?)", (name, login, psw, tm))
            #self.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя" + str(e))
            return False
        return True    
