import psycopg2


# ****************
# Блок обращений к базе
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


allowed_login_characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                            'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                            'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
allowed_password_characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f',
                               'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                               'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '-', '_']


def msg_validate_template(msg):
    validate_result = dict({'msg:': msg, 'token': ''})
    return validate_result

# конец блока

##






