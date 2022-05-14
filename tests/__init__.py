import os
import mysql.connector

CONFIG = {
    'host': os.environ.get('ORM_MYSQL_HOST') or 'localhost',
    'port': os.environ.get('ORM_MYSQL_PORT') or 3307,
    'user': os.environ.get('ORM_MYSQL_USER') or 'root',
    'password': os.environ.get('ORM_MYSQL_PASSWORD') or 'root',
    'database': os.environ.get('ORM_MYSQL_DATABASE') or 'hrushi'
}

mydb = mysql.connector.connect(**CONFIG)
mycursor = mydb.cursor()

mycursor.execute("""
    DROP TABLE IF EXISTS student;
    DROP TABLE IF EXISTS articles;
    DROP TABLE IF EXISTS authors;
    CREATE TABLE student(id int(10) auto_increment PRIMARY KEY, name varchar(15), gender char(1), age int(3));
    Create table articles(id int(10) auto_increment PRIMARY KEY, author_id int(10),title varchar(30), content text);
    Create table authors(id int(10) auto_increment PRIMARY KEY, name varchar(30));
    """)