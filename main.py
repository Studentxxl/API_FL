import sys
sys.path.append("..")
import re
from flask import Flask, request, jsonify
import hashlib
from modules import db_func
from secret import salt
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)


@app.route('/')
def index():
    msg = 'test'
    return jsonify(msg=msg)


# ****************************
# БЛОК РЕГИСТРАЦИИ
# ****************************
@app.route(rule='/register', methods=['POST'])
def register():
    # Формирует словарь из полученного запроса (из json строки)
    request_data = request.get_json()
    """ (комментарий для себя): нужна ли здесь проверка на пустые поля запроса """

    # Получает значения ключей name и password
    login = request_data['login']
    password = request_data['password']

    # * ВАЛИДАЦИЯ логина
    if re.match(pattern=r'^(?=.*[a-z])(?=.*[A-Z])[A-Za-z]{6,}$', string=login) is None:
        msg = 'Поле логин должно быть не меньше 6 символов с латинскими буквами A-Z a-z'
        return jsonify(msg=msg, token='')

    # * ВАЛИДАЦИЯ пароля
    if re.match(pattern=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$', string=password) is None:
        msg = 'Поле пароль должно быть не меньше 8 символов с латинскими буквами A-Z a-z, цифрами 0-9'
        return jsonify(msg=msg, token='')

    # Проверка логина в базе
    base_response = db_func.select(command=f"SELECT login FROM users WHERE login = '{login}'")
    if base_response:
        msg = 'Логин занят'
        return jsonify(msg=msg, token='')
    else:
        # получение last_id
        # Соленый пароль
        salts_password = password + salt.salt
        # Хеш соленого пароля
        salts_password = generate_password_hash(salts_password)
        # Запись в базу
        return_data = db_func.insert_return_id(command=f"INSERT INTO users (login, passhash) "
                                                       f"VALUES ('{login}', '{salts_password}') "
                                                       f"RETURNING id, login, passhash")
        last_id = return_data[0][0]
        last_login = return_data[0][1]
        last_passhash = return_data[0][2]
        # Проверка
        if last_login == login and last_passhash == salts_password:
            # Создание токена сессии (md5)
            token = hashlib.md5(f"{login}".encode()).hexdigest()
            #
            session = db_func.insert_return_id(command=f"INSERT INTO sessions (id, user_id, token) "
                                                       f"VALUES ({last_id}, {last_id}, '{token}') RETURNING token")
            return jsonify(msg='Успешная регистрация', token=f'{session[0][0]}')
        else:
            msg = 'Пользователь не зарегистрирован'
            return jsonify(msg=msg, token='')



if __name__ == "__main__":
    app.run()
