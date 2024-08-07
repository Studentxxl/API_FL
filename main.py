import json
import re
from flask import Flask, request, jsonify
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
        # Запись пользователя в users, получение last_id
        result = func.salts(login=login, password=password)
        if result:
            last_id = result
            # Создание токена сессии (md5)
            token = hashlib.md5(f"{login}".encode()).hexdigest()
            #
            session = func.insert_return_id(command=f"INSERT INTO sessions (id, user_id, token) VALUES ({last_id}, {last_id}, '{token}') RETURNING token")
            return jsonify({'msg': 'Успешная регистрация', 'token': f'{session[0][0]}'})
        else:
            return func.msg_validate_template(msg='Пользователь не зарегистрирован')



if __name__ == "__main__":
    app.run()
