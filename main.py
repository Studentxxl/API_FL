import sys
sys.path.append("..")
from flask import Flask, request, jsonify
import hashlib
from modules import db_func
from modules import valid_token
from secret import salt
from werkzeug.security import generate_password_hash, check_password_hash
from modules import validate

app = Flask(__name__)


def hash_password(pwd):
    salted_password = pwd.encode() + salt.CONST_SALT.encode()
    return hashlib.sha256(salted_password).hexdigest()


@app.route('/')
def index():
    msg = 'test'
    return jsonify(msg=msg)


# ****************************
# БЛОК РЕГИСТРАЦИИ
# ****************************
@app.route(rule='/register', methods=['POST'])
def register():
    # Словарь из POST - запроса
    request_data = request.get_json()

    # Объекты login, password из POST - запроса
    login = request_data['login']
    password = request_data['password']

    # Проверка на тип 'str'
    if isinstance(password, str) and isinstance(login, str):
        # Валидатор
        if (validate.validateWithPattern(validate.Patterns.LOGIN.value, login)
                and validate.validateWithPattern(validate.Patterns.PASSWORD.value, password)):
            # SELECT из базы
            base_response = db_func.select(command=f"SELECT login FROM users WHERE login = '{login}'")

            # Хеш соленого пароля
            if not base_response:
                salts_password = hash_password(password)

                # Запись в базу
                return_data = db_func.insert_return_id(command=f"INSERT INTO users (login, passhash) "
                                                               f"VALUES ('{login}', '{salts_password}') "
                                                               f"RETURNING id, login, passhash")

                if return_data:
                    # Проверка корректности записи в базу
                    if return_data[0][1] == login and return_data[0][2] == salts_password:
                        # Создание сессии, запись в базу
                        generated_hash = generate_password_hash(login)
                        token = generated_hash.split('$')[2]
                        session = db_func.insert_return_id(command=f"INSERT INTO sessions (id, user_id, token) "
                                                                   f"VALUES ({return_data[0][0]}, {return_data[0][0]}, "
                                                                   f"'{token}') RETURNING token")

                        # Проверка корректности записи в базу
                        if session[0][0] == token:
                            return (jsonify(msg='Успешная регистрация', token=f'{session[0][0]}'),
                                    200, {'Content-Type': 'application/json; charset=utf-8'})
                        else:
                            msg = 'Пользователь не зарегистрирован'
                            return (jsonify(msg=msg, token=''),
                                    405, {'Content-Type': 'application/json; charset=utf-8'})
                    else:
                        return (jsonify(msg='', token=''),
                                405, {'Content-Type': 'application/json; charset=utf-8'})
                else:
                    return (jsonify(msg='', token=''),
                            405, {'Content-Type': 'application/json; charset=utf-8'})
            else:
                msg = f'Логин занят'
                return (jsonify(msg=msg, token=''),
                        405, {'Content-Type': 'application/json; charset=utf-8'})
        else:
            msg = f'Логин или пароль неверный'
            return (jsonify(msg=msg, token=''),
                    405, {'Content-Type': 'application/json; charset=utf-8'})
    else:
        return (jsonify(msg='', token=''),
                405, {'Content-Type': 'application/json; charset=utf-8'})




# конец блока регистрации


# ****************************
# БЛОК АУТЕНТИФИКАЦИИ
# ****************************
@app.route(rule='/auth', methods=['POST'])
def auth():
    # Формирует словарь из полученного запроса (из json строки)
    request_data = request.get_json()
    for value in request_data.values():
        if isinstance(value, str):
            return (jsonify({}), 400)

    # Получает значения ключей login и password
    login = request_data['login']
    password = request_data['password']
    # Валидация
    if (validate.validateWithPattern(validate.Patterns.LOGIN.value, login)
            and validate.validateWithPattern(validate.Patterns.PASSWORD.value, password)):
        base_hash = db_func.select(command=f"SELECT passhash FROM users WHERE login = '{login}'")
        if base_hash:
            user_hash = hash_password(pwd=password)
            if base_hash[0][0] == user_hash:

                return jsonify(msg='make session')
            else:
                return jsonify(msg='неверный пароль')
        else:
            return jsonify(msg='нет такого логина')

    return jsonify(msg='n/y')

""" # БЛОК АУТЕНТИФИКАЦИИ НЕ ЗАКОНЧЕН"""
# конец блока аутентификации


# ****************************
# БЛОК ПРОВЕРКИ ТОКЕНА
# ****************************
@app.route(rule='/user_token', methods=['POST'])
def user_token():
    # Словарь из POST - запроса
    request_data = request.get_json()

    # Объекты login, token из POST - запроса
    login = request_data['login']
    token = request_data['token']

    # Проверка токена на тип 'str'
    if isinstance(token, str) and isinstance(login, str):
        # Валидатор
        if validate.validateWithPattern(validate.Patterns.LOGIN.value, login) and token != '':
            # JOIN из базы
            request_result = db_func.select(command=f"SELECT users.id, users.login, sessions.token, "
                                                    f"sessions.date_end FROM users "
                                                    f"JOIN sessions ON users.id = sessions.user_id "
                                                    f"WHERE users.login = '{login}'")
            #  Проверка даты, сравнение токена
            if request_result:
                check_date = valid_token.token_end_date(date=request_result[0][3])
                if check_date == 'date valid' and token == request_result[0][2]:
                    return (jsonify(token=request_result[0][2]),
                            200, {'Content-Type': 'application/json; charset=utf-8'})
                else:
                    return (jsonify(token=''),
                            405, {'Content-Type': 'application/json; charset=utf-8'})
            else:
                return (jsonify(token=''),
                        405, {'Content-Type': 'application/json; charset=utf-8'})
        else:
            return (jsonify(token=''),
                    405, {'Content-Type': 'application/json; charset=utf-8'})
    else:
        return (jsonify(token=''),
                405, {'Content-Type': 'application/json; charset=utf-8'})

# конец блока проверки токена


if __name__ == "__main__":
    app.run()
