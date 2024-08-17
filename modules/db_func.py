import psycopg2
from database import db_config


# ****************
# Блок запросов к базе
# ****************

def makeDBConnect():
    return psycopg2.connect(dbname=db_config.dbname, user=db_config.user, password=db_config.password, host=db_config.host, port=db_config.port)


def connect_with_commit(command):
    '''  '''
    # *
    try:
        conn = makeDBConnect()
        # *
        cursor = conn.cursor()
        cursor.execute(command)
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return result
        # *
    except:
        pass


def connect_without_commit(command):
    '''  '''
    try:
        conn = makeDBConnect()
        # *
        cursor = conn.cursor()
        cursor.execute(command)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except:
        pass

# конец блока










