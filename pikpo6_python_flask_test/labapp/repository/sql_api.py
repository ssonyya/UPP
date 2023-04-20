from typing import List
from labapp import app
import labapp.webservice as webservice
from .connector import StoreConnector
from flask import render_template, make_response, request, jsonify, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import math
import time
from datetime import datetime
#from flask_login import login_user
app.config['SECRET_KEY'] = 'JFNCDNK21N3J'
"""
    В данном модуле реализуется API (Application Programming Interface)
    для взаимодействия с БД с помощью объектов-коннекторов.
    
    ВАЖНО! Методы должны быть названы таким образом, чтобы по названию
    можно было понять выполняемые действия.
"""
#
def check_sort(sort_s):
    if (sort_s == "Возрастанию цены"):
        value_check_sort = "ASC"
    elif (sort_s == "  Убыванию цены   "):
        value_check_sort = "DESC"
    return value_check_sort

def check_price_category(price_category_p):
    if(price_category_p == 'Эконом-класс'):
       value_check_category = 1
    elif (price_category_p == 'Средний-класс'):
        value_check_category = 2
    elif (price_category_p == 'Люкс-класс'):
        value_check_category = 3
    return value_check_category

def check_year(year_y):
    if(year_y == 'до 2010'):
       value_check_year = '< 2010'
    elif (year_y == '2010+'):
        value_check_year = '>= 2010'
    return value_check_year

def check_km(km_k):
    if(km_k == 'до 100.000км'):
       value_check_km = '< 100000'
    elif (km_k == '100.000км+'):
        value_check_km = '>= 100000'
    return value_check_km

def all_none(sort, category, year, km):
    return sort == None and category == None and year == None and km == None

def check_not_none(temp):
    return temp is not None

def select_all_from_source_files(connector: StoreConnector) -> List[tuple]:
    """ Вывод списка обработанных файлов с сортировкой по дате в порядке убывания (DESCENDING) """
    query = f'SELECT * FROM source_files ORDER BY processed DESC'
    result = connector.execute(query).fetchall()
    return result


def select_rows_from_processed_data(connector: StoreConnector, source_file: int) -> List[tuple]:
    """ Выборка строк из таблицы с обработанными данными """
    result = []
    result = connector.execute(f"SELECT processed_data.id, processed_data.name, processed_data.years, processed_data.km_driven, processed_data.selling_price, categories.name FROM processed_data JOIN categories on processed_data.price_category = categories.id WHERE source_file = {source_file} LIMIT 300").fetchall()
    return result

def select_processed_data(connector: StoreConnector, form) -> List[tuple]:
    sort = form.get('sort')
    category = form.get('price_category')
    year = form.get('year')
    km = form.get('km')
    if (all_none(sort, category, year, km)):
        result = connector.execute(f"SELECT * FROM processed_data").fetchall()
    else:        
        pre_query = ""
        if (check_not_none(category)):
            category = check_price_category(category)
            pre_query = pre_query + f"WHERE price_category = {category}"            
        if (check_not_none(year)):
            year = check_year(year)
            if pre_query != "":
                pre_query = pre_query + f" AND years {year}"
            else:
                pre_query = pre_query + f"WHERE years {year}"
        if (check_not_none(km)):
            km = check_km(km)
            if pre_query != "":
                pre_query = pre_query + f" AND km_driven {km}"
            else:
                pre_query = pre_query + f"WHERE km_driven {km}"
        if (check_not_none(sort)):
            sort = check_sort(sort)
            pre_query = pre_query + f" ORDER BY selling_price {sort} " 
        

        query = f'SELECT processed_data.id, processed_data.name, processed_data.years, processed_data.km_driven, processed_data.selling_price, categories.name FROM processed_data JOIN categories on processed_data.price_category = categories.id  {pre_query}  LIMIT 300'
        result = connector.execute(query).fetchall()
    return result

def addUser(connector: StoreConnector, form) -> List[tuple]:
    name = form.get('name')
    login = form.get('login')
    psw = form.get('psw')
    psw2 = form.get('psw2')
    hash = generate_password_hash(psw)
    if len(name) > 4 and len(login) > 4 and len(psw) > 4 and psw == psw2:
        now = datetime.now()
        tm = now.strftime("%Y-%m-%d %H:%M:%S") 
        connector.execute (f"INSERT INTO users (name, login, psw, tm) VALUES {name, login, hash, tm}")
        flash("Вы успешно зарегестрировались", category = "success")
        print("Добавлено в бд")
        return True
    else:
        flash("Ошибка регистрации", category = "error")
        print("Ошибка добавления пользователя")
        return False

def get_user (connector: StoreConnector, login: str = "") -> List[tuple]: 
    result = connector.execute (f"SELECT * FROM users WHERE login = \'{login}\'").fetchall()
    return result


def get_pass_log (connector: StoreConnector, psw: str = "", login: str = "") -> List[tuple]:
    result = connector.execute (f"SELECT * FROM users WHERE login = \'{login}\'").fetchall()
    if len(result) != 0:
        res = (result[0])[3]
        if check_password_hash(res, psw):
            flash("Вы авторизовались", category = "success")
            print("Успешная авторизация")
            return True 
        else:
            flash("Неверный пароль", category = "error")
            print("Неверный пароль")
            return False
    else:
        flash("Нет пользователя с таким логином", category = "error")
        print("Нет пользователя с таким логином") 
        return False 

def get_id (connector: StoreConnector, id: str) -> List[tuple]:
    result = connector.execute (f"SELECT * FROM processed_data WHERE id = \'{id}\'").fetchall() 
    if len(result) != 0:
        flash("Заявка одобрена", category = "success")
        print("Такой автомобиль есть в списке")
    else:
        flash("Такого автомобиля нет в списке", category = "error")        
        print("Такого автомобиля нет в списке") 
        return False       

