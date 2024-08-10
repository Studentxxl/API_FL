import json
import requests
import random
from werkzeug.security import generate_password_hash, check_password_hash


def test_1(login, password):
    response = requests.post(url='http://127.0.0.1:5000/register', json={'login': login, 'password': password})
    responsed = json.loads(response.content)
    return responsed


# ****************************
# БЛОК ВЫЗОВА ТЕСТОВЫХ ФУНКЦИЙ
# ****************************

# тест роута регистрации пользователя '/register'
# (введите значения в поля login и password)
# валидные данные:
# логин: 8-16 символов, латинские буквы
# пароль: 8-16 символов, латинские буквы, цифры 0-9, символы -_
print('результат теста 1:', test_1(login='azAZl09__', password='zA09_+6666666666'))













'''
alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
chars = []
for i in range(48):
    chars.append(random.choice(alphabet))
# Сгенерированная соль
salt = "".join(chars)
hash = generate_password_hash(salt)
print(salt)


def salts(login, password):
    
    # Соленый пароль
    salts_password = password + salt
    # Хеш соленого пароля
    salts_password = generate_password_hash(salts_password)
    # Запись в базу
    return_data = insert_return_id(command=f"INSERT INTO users (login, passhash, salt) "
                                           f"VALUES ('{login}', '{salts_password}', '{salt}') "
                                           f"RETURNING id, login, passhash, salt")
    last_id = return_data[0][0]
    last_login = return_data[0][1]
    last_passhash = return_data[0][2]
    last_salt = return_data[0][3]
    # Проверка
    if last_login == login and last_passhash == salts_password and last_salt == salt:
        return last_id

'''


"""
# * ВАЛИДАЦИЯ логина
    if re.match(pattern=r'^(?=.*[a-z])(?=.*[A-Z])[A-Za-z]{6,}$', string=login) is None:
        msg = 'Поле логин должно быть не меньше 6 символов с латинскими буквами A-Z a-z'
        return jsonify(msg=msg, token='')

    # * ВАЛИДАЦИЯ пароля
    if re.match(pattern=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$', string=password) is None:
        msg = 'Поле пароль должно быть не меньше 8 символов с латинскими буквами A-Z a-z, цифрами 0-9'
        return jsonify(msg=msg, token='')
"""