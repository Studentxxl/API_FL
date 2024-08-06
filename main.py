import json
import re
from flask import Flask, request, make_response, jsonify
import psycopg2
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import func
import hashlib

app = Flask(__name__)


@app.route('/')
def index():
    test_result = func.msg_validate_template(msg='test')
    return test_result

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
    if re.match(pattern=r'^(?=.*[a-z])(?=.*[A-Z])[A-Za-z]{6,}$', string=login) is None:
        msg = 'Поле логин должно быть не меньше 6 символов с латинскими буквами A-Z a-z'
        validate_result = dict({'msg:': msg, 'token': ''})
        json_response = jsonify(validate_result)
        return json_response

    # * ВАЛИДАЦИЯ пароля
    if re.match(pattern=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$', string=password) is None:
        msg = 'Поле пароль должно быть не меньше 8 символов с латинскими буквами A-Z a-z, цифрами 0-9'
        validate_result = dict({'msg:': msg, 'token': ''})
        json_response = jsonify(validate_result)
        return json_response

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
