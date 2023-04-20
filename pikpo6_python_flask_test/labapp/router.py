# Подключаем объект приложения Flask из __init__.py
from labapp import app
# Подключаем библиотеку для "рендеринга" html-шаблонов из папки templates
from flask import Flask, render_template, make_response, request, jsonify, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import labapp.webservice as webservice   # подключаем модуль с реализацией бизнес-логики обработки запросов
from config import DB_URL  
from .repository.connectorfactory import SQLStoreConnectorFactory
#from flask_sqlalchemy import SQLAlchemy
#from flask_login import login_user, login_required


"""
    Модуль регистрации обработчиков маршрутов, т.е. здесь реализуется обработка запросов
    при переходе пользователя на определенные адреса веб-приложения
"""

#Добавляем обработку POST-запроса

db_connector = SQLStoreConnectorFactory().get_connector(DB_URL)
@app.route('/', methods=['POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
   
    """ Обработка запроса к индексной странице """
    # Пример вызова методс выборкой данных из БД и вставка полученных данных в html-шаблон
    processed_files = webservice.get_source_files_list()
    if request.method == 'GET':
         processed_data = webservice.get_processed_data(processed_files[0][0])
    if request.method == 'POST':
         processed_data = webservice.get_files(request.form)
    name = request.cookies.get('auth')     
    # "рендеринг" (т.е. вставка динамически изменяемых данных) в шаблон index.html и возвращение готовой страницы
    return render_template('index.html',
                           title='АВТО',
                           page_name='HOME',
                           ilyas='checked',
                           navmenu=webservice.navmenu,
                           processed_data=processed_data,
                           name = name)


@app.route('/about.html', methods=['GET'])
def about():
    """ Обработка запроса к странице about.html """
    name = request.cookies.get('auth') 
    return render_template('about.html',
                           title='About project',
                           page_name='about',
                           navmenu=webservice.navmenu,
                           name = name)

@app.route('/', methods=['GET'])
@app.route('/glavn.html', methods=['GET'])
def glavn():
    """ Обработка запроса к странице glavn.html """
    return render_template('glavn.html',
                           title='glavn project',
                           page_name='glavn',
                           navmenu=webservice.navmenu)

@app.route('/registr.html', methods=['POST','GET'])
def reg():
    login = request.form.get('login')
    if request.method == 'POST':
        data_user = webservice.get_data_user(login)
        if len(data_user) == 0:
            if webservice.post_msg(request.form):
                return redirect(url_for('avt'))
        else:
            flash("login занят", "error")
            print("login занят")        
    return render_template('registr.html',
                           title='registr project',
                           page_name='registr',
                           navmenu=webservice.navmenu)


@app.route('/avtoriz.html', methods=['POST','GET'])
def avt():
    if request.method == 'POST':
        login = request.form.get('log')
        psw = request.form.get('pass')
        if webservice.get_data_psw_log(psw, login):
            res = make_response(render_template('avtoriz.html',
                                                title='avtoriz project',
                                                page_name='avtoriz',
                                                navmenu=webservice.navmenu,
                                                name = login))
            res.set_cookie('auth', login)
            return res

    return render_template('avtoriz.html',
                           title='avtoriz project',
                           page_name='avtoriz',
                           navmenu=webservice.navmenu)
                     

@app.route('/zayavka.html', methods=['GET', 'POST'])
def zay():
    """ Обработка запроса к странице zayavka.html """
    if request.method == 'POST':
        id = request.form.get('ID')
        kock = request.cookies.get('auth')
        if kock == '':
            flash("Ошибка! Вы не авторизованы", category = "error")
            print("не авторизованы")
        else:
            print("авторизованы")    
            if webservice.get_data_id(id):
                res = make_response(render_template('index.html',
                                                title='avtoriz project',
                                                page_name='avtoriz',
                                                navmenu=webservice.navmenu,
                                                name = id))
                return res   
    name = request.cookies.get('auth') 
    return render_template('zayavka.html',
                           title='zayavka project',
                           page_name='zayavka',
                           navmenu=webservice.navmenu,
                           name = name)

@app.route('/data/<int:source_file_id>', methods=['GET'])
def get_data(source_file_id: int):
    """ Вывод данных по идентификатору обработанного файла """
    processed_data = webservice.get_processed_data(source_file=source_file_id)
    return render_template('data.html',
                           title='MY BEST WEBSERVICE!!1',
                           page_name=f'DATA_FILE_{source_file_id}',
                           navmenu=webservice.navmenu,
                           processed_data=processed_data)


@app.route('/api/contactrequest', methods=['POST'])
def post_contact():
    """ Пример обработки POST-запроса для демонстрации подхода AJAX (см. formsend.js и ЛР№5 АВСиКС) """
    request_data = request.json     # получаeм json-данные из запроса
    # Если в запросе нет данных или неверный заголовок запроса (т.е. нет 'application/json'),
    # или в этом объекте, например, не заполнено обязательное поле 'firstname'
    if not request_data or request_data['firstname'] == '':
        # возвращаем стандартный код 400 HTTP-протокола (неверный запрос)
        return bad_request()
    # Иначе отправляем json-ответ с сообщением об успешном получении запроса
    else:
        msg = request_data['firstname'] + ", ваш запрос получен !"
        return jsonify({'message': msg})


@app.route('/notfound', methods=['GET'])
def not_found_html():
    """ Возврат html-страницы с кодом 404 (Не найдено) """
    return render_template('404.html', title='404', err={'error': 'Not found', 'code': 404})


def bad_request():
    """ Формирование json-ответа с ошибкой 400 протокола HTTP (Неверный запрос) """
    return make_response(jsonify({'message': 'Bad request !'}), 400)
