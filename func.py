import psycopg2

dbname = 'postgres'
user = 'postgres'
password = 'RTy567'
host = 'localhost'


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




