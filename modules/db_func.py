import psycopg2
from database import db_config


# ****************
# Блок запросов к базе
# ****************


def insert_return_id(command):
    '''  '''
    # *
    try:
        conn = psycopg2.connect(dbname=db_config.dbname, user=db_config.user, password=db_config.password, host=db_config.host)
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
        conn = psycopg2.connect(dbname=db_config.dbname, user=db_config.user, password=db_config.password, host=db_config.host)
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
    conn = psycopg2.connect(dbname=db_config.dbname, user=db_config.user, password=db_config.password, host=db_config.host)
    # *
    cursor = conn.cursor()
    cursor.execute(command)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# конец блока










