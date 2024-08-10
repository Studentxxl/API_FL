import sys
sys.path.append("..")
from flask import Flask, request, jsonify
import hashlib
from modules import db_func
from secret import salt
from werkzeug.security import generate_password_hash, check_password_hash
from modules import validate

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
    # Валидация
    if (validate.validateWithPattern(validate.Patterns.LOGIN.value, login)
            and validate.validateWithPattern(validate.Patterns.PASSWORD.value, password)):
        # Проверка логина в базе
        base_response = db_func.select(command=f"SELECT login FROM users WHERE login = '{login}'")
        if base_response:
            msg = 'Логин занят'
            return jsonify(msg=msg, token='')
        else:
            # Соленый пароль
            salts_password = password + salt.salt
            # Хеш соленого пароля
            salts_password = generate_password_hash(salts_password)
            # Запись в базу
            return_data = db_func.insert_return_id(command=f"INSERT INTO users (login, passhash) "
                                                           f"VALUES ('{login}', '{salts_password}') "
                                                           f"RETURNING id, login, passhash")
            """ (комментарий для себя): здесь будет ошибка, если db_func.insert_return_id не вернет ничего """
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
                """ (комментарий для себя): здесь будет ошибка, если db_func.insert_return_id не вернет ничего """
                return jsonify(msg='Успешная регистрация', token=f'{session[0][0]}')
            else:
                msg = 'Пользователь не зарегистрирован'
                return jsonify(msg=msg, token='')
    else:
        msg = 'Логин или пароль неверный'
        return jsonify(msg=msg, token='')
# конец блока регистрации


if __name__ == "__main__":
    app.run()
