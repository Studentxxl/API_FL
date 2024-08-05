import json
import requests
import psycopg2


def test_1(login, password):
    response = requests.post(url='http://127.0.0.1:5000/register', json={'login': login, 'password': password})
    dct = json.loads(response.text)
    return dct


# ****************************
# БЛОК ВЫЗОВА ТЕСТОВЫХ ФУНКЦИЙ
# ****************************

# тест роута регистрации пользователя '/register'
# (введите значения в поля login и password)
# валидные данные:
# логин: 8-16 символов, латинские буквы
# пароль: 8-16 символов, латинские буквы, цифры 0-9, символы -_
print('результат теста 1:', test_1(login='qwertyui', password='12345678'))