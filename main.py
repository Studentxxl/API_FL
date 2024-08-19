import sys
sys.path.append("..")
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
from modules import characters_validate
from modules import db_func
from modules import answer
from modules import field_validate
from modules import hash

app = Flask(__name__)


@app.route('/')
def index():
    msg = ''
    return jsonify(msg=msg)


# ****************************
# БЛОК РЕГИСТРАЦИИ
# ****************************
@app.route(rule='/register', methods=['POST'])
def register():
    # Словарь из POST - запроса
    request_data = request.get_json()

    # Проверка наличия полей 'login' 'password', проверка на тип 'str'
    result = field_validate.check_fields_in_dict(field_1='login', field_2='password', dct=request_data)
    if result:
        login = result[0]
        password = result[1]

        # Валидатор
        if (characters_validate.validateWithPattern(characters_validate.Patterns.LOGIN.value, login)
                and characters_validate.validateWithPattern(characters_validate.Patterns.PASSWORD.value, password)):
            # SELECT из базы
            base_response = db_func.connect_without_commit(command=f"SELECT login FROM users "
                                                                   f"WHERE login = '{login}'")

            # Хеш соленого пароля
            if not base_response:
                salts_password = hash.hash_password(pwd=password)

                # Запись в базу
                return_data = db_func.connect_with_commit(command=f"INSERT INTO users (login, passhash) "
                                                                  f"VALUES ('{login}', '{salts_password}') "
                                                                  f"RETURNING id, login, passhash")

                if return_data:
                    # Проверка корректности записи в базу
                    if return_data[0][1] == login and return_data[0][2] == salts_password:
                        # Создание сессии, запись в базу
                        generated_hash = generate_password_hash(login)
                        token = generated_hash.split('$')[2]
                        session = db_func.connect_with_commit(command=f"INSERT INTO sessions (id, user_id, token) "
                                                                      f"VALUES ({return_data[0][0]}, {return_data[0][0]}, "
                                                                      f"'{token}') RETURNING token")

                        # Проверка корректности записи в базу
                        if token == session[0][0]:
                            msg = 'Успешная регистрация'
                            return answer.for_frontend(msg=msg, token=session[0][0], code=200)
                        else:
                            msg = 'Пользователь не зарегистрирован'
                            return answer.for_frontend(msg=msg)
                    else:
                        return answer.for_frontend()
                else:
                    return answer.for_frontend()
            else:
                msg = f'Логин занят'
                return answer.for_frontend(msg=msg)
        else:
            msg = f'Неверный логин или пароль'
            return answer.for_frontend(msg=msg)
    else:
        return answer.for_frontend()

# конец блока регистрации


# ****************************
# БЛОК АУТЕНТИФИКАЦИИ
# ****************************
@app.route(rule='/auth', methods=['POST'])
def auth():
    # Словарь из POST - запроса
    request_data = request.get_json()

    # Проверка наличия полей 'login' 'password', проверка на тип 'str'
    result = field_validate.check_fields_in_dict(field_1='login', field_2='password', dct=request_data)
    if result:
        login = result[0]
        password = result[1]

        # Валидация
        if (characters_validate.validateWithPattern(characters_validate.Patterns.LOGIN.value, login)
                and characters_validate.validateWithPattern(characters_validate.Patterns.PASSWORD.value, password)):
            base_response = db_func.connect_without_commit(command=f"SELECT passhash, id "
                                                                   f"FROM users "
                                                                   f"WHERE login = '{login}'")
            if base_response:
                user_hash = hash.hash_password(pwd=password)
                if base_response[0][0] == user_hash:
                    # Создание сессии, запись в базу
                    generated_hash = generate_password_hash(login)
                    token = generated_hash.split('$')[2]
                    command = f"""UPDATE sessions SET token = '{token}', 
                    date_start = CURRENT_TIMESTAMP, 
                    date_end = CURRENT_TIMESTAMP + '7 days'::interval 
                    WHERE id = {base_response[0][1]} RETURNING token"""
                    session = db_func.connect_with_commit(command=command)

                    # Проверка корректности записи в базу
                    if token == session[0][0]:
                        return answer.for_frontend(token=session[0][0], code=200)
                    else:
                        return answer.for_frontend()
                else:
                    return answer.for_frontend()
            else:
                return answer.for_frontend()
        else:
            msg = 'Неверный логин или пароль'
            return answer.for_frontend(msg=msg)
    else:
        return answer.for_frontend()

# конец блока аутентификации


# ****************************
# БЛОК ПРОВЕРКИ ТОКЕНА
# ****************************
@app.route(rule='/user_token', methods=['POST'])
def user_token():
    # Словарь из POST - запроса
    request_data = request.get_json()

    # Проверка наличия полей 'login' 'token', проверка на тип 'str'
    result = field_validate.check_fields_in_dict(field_1='login', field_2='token', dct=request_data)
    if result:
        login = result[0]
        token = result[1]

        # Валидатор
        if characters_validate.validateWithPattern(characters_validate.Patterns.LOGIN.value, login) and token != '':
            # JOIN из базы
            command = f"""SELECT users.id, users.login, sessions.token, sessions.date_end 
            FROM users JOIN sessions ON users.id = sessions.user_id 
            WHERE users.login = '{login}' AND sessions.token = '{token}'
            AND date_end > CURRENT_TIMESTAMP"""
            request_result = db_func.connect_without_commit(command=command)
            #  Проверка даты, сравнение токена
            if request_result:
                if token == request_result[0][2]:
                    return answer.for_frontend(token=request_result[0][2], code=200)
                else:
                    return answer.for_frontend()
            else:
                return answer.for_frontend()
        else:
            return answer.for_frontend()
    else:
        return answer.for_frontend()

# конец блока проверки токена


if __name__ == "__main__":
    app.run()
