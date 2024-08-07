import psycopg2
import json
from flask import jsonify
import re
from enum import Enum
import random
from werkzeug.security import generate_password_hash

# ****************
# Блок запросов к базе
# ****************


dbname = 'postgres'
user = 'postgres'
password = 'RTy567'
host = 'localhost'


def insert_return_id(command):
    '''  '''
    # *
    try:
        conn = psycopg2.connect(dbname='postgres', user='postgres', password='RTy567', host='localhost')
        # *
        cursor = conn.cursor()
        cursor.execute(command)
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return result
        # *
    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")


def insert(command):
    '''  '''
    # *
    try:
        conn = psycopg2.connect(dbname='postgres', user='postgres', password='RTy567', host='localhost')
        # *
        cursor = conn.cursor()
        cursor.execute(command)
        conn.commit()
        cursor.close()
        conn.close()
        # *
    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")


def select(command):
    '''  '''
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='RTy567', host='localhost')
    # *
    cursor = conn.cursor()
    cursor.execute(command)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# конец блока


# ****************
# Блок валидации
# ****************


def msg_validate_template(msg):
    validate_result = dict({'msg:': msg, 'token': ''})
    json_response = jsonify(validate_result)
    return json_response


# конец блока


# ****************
# Блок SALT
# ****************


def salts(login, password):
    '''
    Генерирует соль, добавляет к паролю, хеширует результат.
    Пишет в таблицу users логин, хеш соленого пароля, соль.
    Проверяет правильность записи.
    Возвращает last_id базы
    '''
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars = []
    for i in range(25):
        chars.append(random.choice(alphabet))
    # Сгенерированная соль
    salt = "".join(chars)
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


def unsalt():
    pass


# конец блока






