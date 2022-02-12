import pytest
import os
from orm import Table, has_many, belongs_to


CONFIG = {
    'host': os.environ.get('ORM_MYSQL_HOST') or 'localhost',
    'port': os.environ.get('ORM_MYSQL_PORT') or 3306,
    'user': os.environ.get('ORM_MYSQL_USER'),
    'password': os.environ.get('ORM_MYSQL_PASSWORD'),
    'database': os.environ.get('ORM_MYSQL_DATABASE')
}

print(CONFIG)
Table.connect(config_dict=CONFIG)
"""
Table student with following schema is alredy created in db

+--------+-------------+------+-----+---------+----------------+
| Field  | Type        | Null | Key | Default | Extra          |
+--------+-------------+------+-----+---------+----------------+
| id     | int(10)     | NO   | PRI | NULL    | auto_increment |
| name   | varchar(15) | NO   |     | NULL    |                |
| gender | char(1)     | YES  |     | NULL    |                |
| age    | int(3)      | YES  |     | NULL    |                |
+--------+-------------+------+-----+---------+----------------+
"""

class Student(Table):
    table_name = 'student'

def test_connection():
    assert Student.cursor is not None, "connection should me made"

def test_schema():
    assert Student.column_names == ['id', 'name', 'gender', 'age']

def test__init__():
    """
    Test attributes are initialized properly
    """
    new_stu = Student(name='test-name', age=20, gender='F')
    assert new_stu.name == 'test-name'
    assert new_stu.age == 20
    assert new_stu.gender == 'F'

def test_save():
    new_stu = Student(name='test-name', age=21, gender='F')
    new_stu.save()
    assert new_stu.primary_key_value() is not None

def test_create():
    new_stu = Student.create(name='test-name', age=22, gender='M')
    assert isinstance(new_stu, Student)
    assert new_stu.primary_key_value() is not None

def test_update():
    new_stu = Student.create(name='test-name', age=22, gender='M')
    assert isinstance(new_stu, Student)
    
    new_stu.update(name="new-name", age=20)

    updated_stu = Student.find(new_stu.id)
    assert updated_stu.name == "new-name" and updated_stu.age == 20

def test_find():
    new_stu = Student.create(name='test-name', age=22, gender='M')
    pk_value = new_stu.primary_key_value()
    assert Student.find(pk_value) == new_stu

def test_destroy():
    new_stu = Student.create(name='test-name', age=23, gender='f')
    pk_value = new_stu.primary_key_value()

    new_stu.destroy()

    # assert record is deleted
    assert Student.find(pk_value) is None

"""
    --extra-index-url
    CREATE TABLE student(id int(10) auto_increment PRIMARY KEY, name varchar(15), gender char(1), age int(3));

    CONFIG = {
        'host': "sql6.freemysqlhosting.net",
        'port': "3306",
        'user': "sql6471929",
        'password': "n6sA2BD5Hk",
        'database': "sql6471929"
    }
"""
