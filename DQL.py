import mysql.connector
from config import *

def get_teachers(user_id):
    conn = mysql.connector.connect( **database_config, database=database_name)
    cur = conn.cursor(dictionary=True)
    SQL_Query='select * from teachers where cid=%s '
    cur.execute(SQL_Query,(user_id,))
    data=cur.fetchone()
    cur.close()
    conn.close()
    return data

def get_admin(user_id):
    conn = mysql.connector.connect( **database_config, database=database_name)
    cur = conn.cursor(dictionary=True)
    SQL_Query='select * from admin where cid=%s '
    cur.execute(SQL_Query,(user_id,))
    data=cur.fetchone()
    cur.close()
    conn.close()
    return data


def get_file_by_id(file_id):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor(dictionary=True)
    SQL_Query = 'select * from files where id = %s'
    cur.execute(SQL_Query, (file_id,))
    data = cur.fetchone()
    cur.close()
    conn.close()
    return data