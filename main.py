from flask import Flask, request, make_response
import psycopg2
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import func

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello! I am API'


@app.route(rule='/register', methods=['POST'])
def register():
    # Формирует словарь из полученного запроса (из json строки)
    request_data = request.get_json()

    # Получает значения ключей name и password
    login = request_data['login']
    password = request_data['password']

    # * ВАЛИДАЦИЯ
    #
    validate_result = {}
    # разрешенные символы
    allowed_login_characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                                'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                                'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    allowed_password_characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f',
                                   'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                                   'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                                   'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '-', '_']
    # Проверка длины логина
    if len(login) < 8 or len(login) > 16:
        validate_result['login_length'] = len(login)
    # Проверка символов логина
    forbidden_login_characters = ''
    for character in login:
        if character not in allowed_login_characters:
            forbidden_login_characters += character
    if forbidden_login_characters:
        validate_result['forbidden_login_characters'] = forbidden_login_characters

    # Если не прошла проверка логина - возвращает ошибки и пустой токен
    if validate_result:
        validate_result['token'] = ''
        return validate_result

    # Проверка длины пароля
    if len(password) < 8 or len(password) > 16:
        validate_result['password_length'] = len(password)
    # Проверка символов пароля
    forbidden_password_characters = ''
    for character in password:
        if character not in allowed_password_characters:
            forbidden_password_characters += character
    if forbidden_password_characters:
        validate_result['forbidden_password_characters'] = forbidden_password_characters

    # Если не прошла проверка пароля - возвращает ошибки и пустой токен
    if validate_result:
        validate_result['token'] = ''
        return validate_result

    # Проверка логина в базе
    exist_login = {}
    login_query = f"SELECT login FROM users WHERE login = '{login}'"
    base_response = func.select(command=login_query)
    if base_response:
        exist_login['exist_login'] = base_response[0][0]
        exist_login['token'] = ''
        return exist_login
    if exist_login == {}:
        # ХЕШИРОВАНИЕ ПАРОЛЯ (если в базе нет логина)
        hashed_password = generate_password_hash(password)

        # Создание токена сессии (md5)

        # Запись в базу

        # Ответ фронтенду


        return {}


# hash = generate_password_hash('2w23e34')
# check_password_hash(hash, '2w2e34')



if __name__ == "__main__":
    app.run()
