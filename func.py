import psycopg2
import json


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
    json_response = json.dumps(validate_result)
    return json_response

# конец блока






