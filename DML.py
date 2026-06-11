import mysql.connector
from config import *

def insert_into_teachers(cid, name, last_name, phone, username, password):
    conn = mysql.connector.connect( **database_config, database=database_name)
    cur = conn.cursor()
    SQL_Query='insert into teachers (cid, name, last_name, phone,username, password) values (%s,%s, %s, %s,%s,%s)'
    cur.execute(SQL_Query,(cid, name, last_name, phone,username, password))
    user_id=cur.lastrowid
    conn.commit()
    cur.close()
    conn.close()
    return user_id

def insert_into_admin(cid,name, last_name, phone, username, password):
    conn = mysql.connector.connect( **database_config, database=database_name)
    cur = conn.cursor()
    SQL_Query='insert into admin (cid,name, last_name, phone,username, password) values (%s,%s, %s, %s,%s,%s)'
    cur.execute(SQL_Query,(cid,name, last_name, phone,username, password))
    conn.commit()
    cur.close()
    conn.close()

def insert_into_files(teacher_id , file_name , class_name , period , display_date):
    conn = mysql.connector.connect( **database_config, database=database_name)
    cur = conn.cursor()
    SQL_Query='insert into files (teacher_id , file_name ,  class_name , period , display_date) values ( %s, %s, %s,%s,%s)'
    cur.execute(SQL_Query,( teacher_id , file_name ,  class_name , period , display_date))
    fid=cur.lastrowid
    conn.commit()
    cur.close()
    conn.close()
    return fid

def insert_into_daily_queue( file_id, display_date):
    conn = mysql.connector.connect( **database_config, database=database_name)
    cur = conn.cursor()
    SQL_Query='insert into  daily_queue (file_id, display_date) VALUES (%s, %s)'
    cur.execute(SQL_Query,( file_id, display_date))
    conn.commit()
    cur.close()
    conn.close()
