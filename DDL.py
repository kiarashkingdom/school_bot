import mysql.connector
from config import *

def create_and_drop_database(db_name):
    conn = mysql.connector.connect( **database_config)
    cur = conn.cursor()
    cur.execute(f'drop database if exists {db_name};')
    cur.execute(f'create database if not exists {db_name};')
    conn.commit()
    cur.close()
    conn.close()

def create_admin_table(db_name):
    conn = mysql.connector.connect(**database_config, database=db_name)
    cur = conn.cursor()
    sql_query = '''
    create table admin (
    `CID` int   not null primary key,
    `name` varchar(50),
    `last_name` varchar(50),
    `phone` varchar(50),
    `username` varchar(50) unique not null,
    `password` varchar(255) not null,
    `register_date` datetime default current_timestamp)
    '''
    cur.execute(sql_query)
    conn.commit()
    cur.close()
    conn.close()


def create_teachers_table(db_name):
    conn = mysql.connector.connect( **database_config, database=db_name)
    cur = conn.cursor()
    SQL_Query = '''
create table teachers (
    `CID` int  not null primary key,
    `name` varchar(50), 
    `last_name` varchar(50),
    `phone` varchar(50),
    `username` varchar(50) unique not null,
    `password` varchar(255) not null,
    `register_date` datetime default current_timestamp,
    `last_update` datetime default current_timestamp on update current_timestamp)
'''
    cur.execute(SQL_Query)
    conn.commit()
    cur.close()
    conn.close()


def create_files_table(db_name):
    conn = mysql.connector.connect(**database_config, database=db_name)
    cur = conn.cursor()
    sql_query = '''
    create table files (
    `ID` int auto_increment primary key,
    `teacher_id` int not null,
    `file_name` varchar(50),
    `class_name`  varchar(50) not null,
    `period` varchar(50) not null,
    `display_date` date not null,
    `upload_date` datetime default current_timestamp,
    foreign key (`teacher_id`) references teachers(`CID`))
    '''
    cur.execute(sql_query)
    conn.commit()
    cur.close()
    conn.close()


def create_daily_queue_table(db_name):
    conn = mysql.connector.connect(**database_config, database=db_name)
    cur = conn.cursor()
    sql_query = '''
    create table daily_queue (
    `ID` int auto_increment primary key,
    `file_id` int not null,
    `display_date` date not null,
    foreign key (`file_id`) references files(`ID`) )
    '''
    cur.execute(sql_query)
    conn.commit()
    cur.close()
    conn.close()

if __name__== '__main__':
    db_name= database_name
    create_and_drop_database(db_name)
    create_teachers_table(db_name)
    create_files_table(db_name)
    create_admin_table(db_name)
    create_daily_queue_table(db_name)