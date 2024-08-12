import sys
sys.path.append("..")
from flask import Flask, request, jsonify
import hashlib
from modules import db_func
from secret import salt
from werkzeug.security import generate_password_hash, check_password_hash
from modules import validate

app = Flask(__name__)


def hash_password(pwd):
    salted_password = pwd.encode() + salt.CONST_SALT.encode()
    return hashlib.sha256(salted_password).hexdigest()


def check_password(pwd, hashed):
    return hashed == hash_password(pwd)


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

    for value in request_data.values():
        if type(value) != str:
            return (jsonify({}), 400)

    # Получает значения ключей login и password
    login = request_data['login']
    password = request_data['password']
    # Валидация
    if (validate.validateWithPattern(validate.Patterns.LOGIN.value, login)
            and validate.validateWithPattern(validate.Patterns.PASSWORD.value, password)):
        # Проверка логина в базе
        base_response = db_func.select(command=f"SELECT login FROM users WHERE login = '{login}'")
        if base_response:
            msg = 'Логин занят'
            return (jsonify(msg=msg, token=''),
                    405, {'Content-Type': 'application/json; charset=utf-8'})
        else:
            # Мы не используем generate_password_hash со статичной солью
            salts_password = hash_password(password)

            # Запись в базу
            return_data = db_func.insert_return_id(command=f"INSERT INTO users (login, passhash) "
                                                           f"VALUES ('{login}', '{salts_password}') "
                                                           f"RETURNING id, login, passhash")
            """ (комментарий для себя): здесь будет ошибка, если db_func.insert_return_id не вернет ничего """
            # Все ошибки нужно обрабатывать!!!

            last_id = return_data[0][0]
            last_login = return_data[0][1]
            last_passhash = return_data[0][2]

            # Проверка
            if last_login == login and last_passhash == salts_password:
                # а вот здесь случайная соль из generate_password_hash как раз кстати
                generated_hash = generate_password_hash(login)
                # нам нужна только третья часть строки
                token = generated_hash.split('$')[2]

                session = db_func.insert_return_id(command=f"INSERT INTO sessions (id, user_id, token) "
                                                           f"VALUES ({last_id}, {last_id}, '{token}') RETURNING token")
                """ (комментарий для себя): здесь будет ошибка, если db_func.insert_return_id не вернет ничего """
                return (jsonify(msg='Успешная регистрация', token=f'{session[0][0]}'),
                        200, {'Content-Type': 'application/json; charset=utf-8'})
            else:
                msg = 'Пользователь не зарегистрирован'
                return (jsonify(msg=msg, token=''),
                        405, {'Content-Type': 'application/json; charset=utf-8'})
    else:
        msg = f'Логин или пароль неверный'
        return (jsonify(msg=msg, token=''),
                405, {'Content-Type': 'application/json; charset=utf-8'})


# конец блока регистрации


# ****************************
# БЛОК АУТЕНТИФИКАЦИИ
# ****************************
@app.route(rule='/auth', methods=['POST'])
def auth():
    # Формирует словарь из полученного запроса (из json строки)
    request_data = request.get_json()

    """Проверка на тип *строка*???"""

    # Получает значения ключей login и password
    login = request_data['login']
    password = request_data['password']
    # Валидация
    if (validate.validateWithPattern(validate.Patterns.LOGIN.value, login)
            and validate.validateWithPattern(validate.Patterns.PASSWORD.value, password)):
        passhash = db_func.select(command=f"SELECT passhash FROM users WHERE login = '{login}'")
        #passhash[0][0]








# конец блока аутентификации

if __name__ == "__main__":
    app.run()
