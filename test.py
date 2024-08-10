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
print('результат теста 1:', test_1(login='fqwQll', password='qqqgqqqqqq123Q'))













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