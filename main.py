import json

from flask import Flask, request, make_response
import psycopg2
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import func
import hashlib

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello! I am API'

# ****************************
# БЛОК РЕГИСТРАЦИИ
# ****************************
@app.route(rule='/register', methods=['POST'])
def register():
    # Формирует словарь из полученного запроса (из json строки)
    request_data = request.get_json()

    # Получает значения ключей name и password
    login = request_data['login']
    password = request_data['password']

    # * ВАЛИДАЦИЯ логина
    if len(login) < 8 or len(login) > 16:
        return func.msg_validate_template(msg='Длина логина должна быть от 8 до 16')

    invalid_login_characters = ''
    for character in login:
        if character not in func.allowed_login_characters:
            invalid_login_characters += character
    if invalid_login_characters:
        return func.msg_validate_template(msg='Недопустимые символы в поле <логин>')

    # * ВАЛИДАЦИЯ пароля
    if len(password) < 8 or len(password) > 16:
        return func.msg_validate_template(msg='Длина пароля должна быть от 8 до 16')

    invalid_password_characters = ''
    for character in password:
        if character not in func.allowed_password_characters:
            invalid_password_characters += character
    if invalid_password_characters:
        return func.msg_validate_template(msg='Недопустимые символы в поле <пароль>')

    # Проверка логина в базе
    base_response = func.select(command=f"SELECT login FROM users WHERE login = '{login}'")
    if base_response:
        return func.msg_validate_template(msg='Логин занят')
    else:
        # хеш пароля
        hashed_password = generate_password_hash(password)

        # Запись нового пользователя в базу, проверка записи
        return_data = func.insert_return_id(command=f"INSERT INTO users (login, passhash) VALUES ('{login}', "
                                                    f"'{hashed_password}') RETURNING id, login, passhash")
        #
        last_id = return_data[0][0]
        last_login = return_data[0][1]
        last_passhash = return_data[0][2]
        if last_login == login and last_passhash == hashed_password:
            # Создание токена сессии (md5)
            token = hashlib.md5(f"{login}".encode()).hexdigest()
            #
            session = func.insert_return_id(command=f"INSERT INTO sessions (id, user_id, token) VALUES ({last_id}, {last_id}, '{token}') RETURNING token")
            return json.dumps({'msg': 'Успешная регистрация', 'token': f'{session[0][0]}'})
        else:
            return func.msg_validate_template(msg='Пользователь не зарегистрирован')


# check_password_hash(hash, '2w2e34')

if __name__ == "__main__":
    app.run()
